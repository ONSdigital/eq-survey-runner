from typing import List, Mapping

from structlog import get_logger

from app.data_model.answer_store import AnswerStore
from app.data_model.progress_store import ProgressStore
from app.data_model.list_store import ListStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules import (
    evaluate_goto,
    evaluate_skip_conditions,
    is_goto_rule,
)

logger = get_logger()


class PathFinder:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        metadata: Mapping,
        progress_store: ProgressStore = None,
        list_store: ListStore = None,
    ):
        self.answer_store = answer_store
        self.metadata = metadata
        self.schema = schema
        self.progress_store = progress_store
        self.list_store = list_store

    def is_path_complete(self, path):
        return not self.get_first_incomplete_location(path)

    def get_first_incomplete_location(self, path):
        if path:
            first_location = path[0]
            section_id = self.schema.get_section_id_for_block_id(
                first_location.block_id
            )

            for location in path:
                block = self.schema.get_block(location.block_id)
                block_type = block.get('type')
                if location not in self.progress_store.get_completed_locations(
                    section_id
                ) and block_type not in ['SectionSummary', 'Summary', 'Confirmation']:
                    return location

        return None

    def full_routing_path(self):
        path = []
        sections = self.schema.get_sections()
        for section in sections:
            path = path + list(self.routing_path(section))
        return path

    def routing_path(self, section: Mapping) -> RoutingPath:
        """
        Visits all the blocks in a section and returns a path given a list of answers.
        """
        blocks: List[Mapping] = []
        path: List[Location] = []

        for group in section['groups']:
            if 'skip_conditions' in group:
                if evaluate_skip_conditions(
                    group['skip_conditions'],
                    self.schema,
                    self.metadata,
                    self.answer_store,
                    self.list_store,
                    routing_path=path,
                ):
                    continue

            blocks.extend(group['blocks'])

        if blocks:
            path = self._build_path(blocks, path)

        return RoutingPath(path)

    @staticmethod
    def _block_index_for_block_id(blocks, block_id):
        return next(
            (index for (index, block) in enumerate(blocks) if block['id'] == block_id),
            None,
        )

    def _build_path(self, blocks, path):
        # Keep going unless we've hit the last block
        block_index = 0
        while block_index < len(blocks):
            block = blocks[block_index]

            is_skipping = block.get('skip_conditions') and evaluate_skip_conditions(
                block['skip_conditions'],
                self.schema,
                self.metadata,
                self.answer_store,
                self.list_store,
                routing_path=path,
            )

            if not is_skipping:
                this_location = Location(block_id=block['id'])

                if this_location not in path:
                    path.append(this_location)

                # If routing rules exist then a rule must match (i.e. default goto)
                routing_rules = block.get('routing_rules')
                if routing_rules:
                    block_index = self._evaluate_routing_rules(
                        this_location, blocks, routing_rules, block_index, path
                    )
                    if block_index:
                        continue

                    # Return path if routing out of a section
                    return path

            # Last block so return path
            if block_index == len(blocks) - 1:
                return path

            # No routing rules, so step forward a block
            block_index = block_index + 1

    def _evaluate_routing_rules(
        self, this_location, blocks, routing_rules, block_index, path
    ):
        for rule in filter(is_goto_rule, routing_rules):
            should_goto = evaluate_goto(
                rule['goto'],
                self.schema,
                self.metadata,
                self.answer_store,
                self.list_store,
                routing_path=path,
            )

            if should_goto:
                next_block_id = self._get_next_block_id(rule)
                next_block_index = PathFinder._block_index_for_block_id(
                    blocks, next_block_id
                )
                next_precedes_current = (
                    next_block_index is not None and next_block_index < block_index
                )

                if next_precedes_current:
                    self._remove_rule_answers(rule['goto'], this_location)
                    next_location = Location(block_id=next_block_id)
                    path.append(next_location)
                    return None

                return next_block_index

    def _get_next_block_id(self, rule):
        if 'group' in rule['goto']:
            return self.schema.get_first_block_id_for_group(rule['goto']['group'])
        return rule['goto']['block']

    def _remove_rule_answers(self, goto_rule, this_location):
        # We're jumping backwards, so need to delete all answers from which
        # route is derived. Need to filter out conditions that don't use answers
        if 'when' in goto_rule.keys():
            for condition in goto_rule['when']:
                if 'meta' not in condition.keys():
                    self.answer_store.remove_answer(condition['id'])

        section_id = self.schema.get_section_id_for_block_id(this_location.block_id)

        self.progress_store.remove_completed_location(section_id, this_location)
