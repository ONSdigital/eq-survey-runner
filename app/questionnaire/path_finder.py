from typing import List, Mapping

from structlog import get_logger

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore
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
            for location in path:
                block = self.schema.get_block(location.block_id)
                block_type = block.get('type')

                is_location_complete = (
                    location
                    in self.progress_store.get_completed_locations(
                        section_id=location.section_id,
                        list_item_id=location.list_item_id,
                    )
                )

                if not is_location_complete and block_type not in [
                    'SectionSummary',
                    'Summary',
                    'Confirmation',
                ]:
                    return location

        return None

    def full_routing_path(self, sections=None):
        path = []
        schema_sections = sections or self.schema.get_sections()

        for section_schema in schema_sections:
            section_id = section_schema['id']
            for_list = self.schema.get_repeating_list_for_section(section_id)

            if for_list:
                for list_item_id in self.list_store[for_list].items:
                    path = path + list(
                        self.routing_path(
                            section_id=section_id, list_item_id=list_item_id
                        )
                    )
            else:
                path = path + list(self.routing_path(section_id=section_id))

        return path

    def routing_path(self, section_id, list_item_id=None) -> RoutingPath:
        """
        Visits all the blocks in a section and returns a path given a list of answers.
        """
        blocks: List[Mapping] = []
        path: List[Location] = []
        section_schema = self.schema.get_section(section_id)

        for group in section_schema['groups']:
            if 'skip_conditions' in group:
                if evaluate_skip_conditions(
                    group['skip_conditions'],
                    self.schema,
                    self.metadata,
                    self.answer_store,
                    self.list_store,
                    list_item_id=list_item_id,
                    routing_path=path,
                ):
                    continue

            blocks.extend(group['blocks'])

        if blocks:
            path = self._build_path(blocks, path, section_id, list_item_id)

        return RoutingPath(path)

    @staticmethod
    def _block_index_for_block_id(blocks, block_id):
        return next(
            (index for (index, block) in enumerate(blocks) if block['id'] == block_id),
            None,
        )

    def _build_path(self, blocks, path, section_id, list_item_id=None):
        # Keep going unless we've hit the last block
        block_index = 0
        for_list = self.schema.get_repeating_list_for_section(section_id)
        while block_index < len(blocks):
            block = blocks[block_index]

            is_skipping = block.get('skip_conditions') and evaluate_skip_conditions(
                block['skip_conditions'],
                self.schema,
                self.metadata,
                self.answer_store,
                self.list_store,
                list_item_id=list_item_id,
                routing_path=path,
            )

            if not is_skipping:
                if for_list and list_item_id:
                    this_location = Location(
                        section_id=section_id,
                        block_id=block['id'],
                        list_name=for_list,
                        list_item_id=list_item_id,
                    )
                else:
                    this_location = Location(
                        section_id=section_id, block_id=block['id']
                    )

                if this_location not in path:
                    path.append(this_location)

                # If routing rules exist then a rule must match (i.e. default goto)
                routing_rules = block.get('routing_rules')
                if routing_rules:
                    block_index = self._evaluate_routing_rules(
                        this_location,
                        blocks,
                        routing_rules,
                        block_index,
                        path,
                        list_item_id=list_item_id,
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
        self, this_location, blocks, routing_rules, block_index, path, list_item_id=None
    ):
        for rule in filter(is_goto_rule, routing_rules):
            should_goto = evaluate_goto(
                rule['goto'],
                self.schema,
                self.metadata,
                self.answer_store,
                self.list_store,
                list_item_id=list_item_id,
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
