from datetime import datetime
from typing import Optional

from structlog import get_logger

from app.data_model.progress_store import CompletionStatus
from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.router import Router

logger = get_logger()


class BlockHandler:
    def __init__(
        self, schema, questionnaire_store, language, current_location, request_args
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language
        self._current_location = current_location
        self._request_args = request_args or {}
        self.block = self._schema.get_block(current_location.block_id)

        self._questionnaire_store_updater = None
        self._path_finder = None
        self._placeholder_renderer = None
        self._router = None
        self._routing_path = self._get_routing_path()
        self.form = None
        self.page_title = None

        if not self.is_location_valid():
            raise InvalidLocationException(
                f'location {self._current_location} is not valid'
            )

    @property
    def current_location(self):
        return self._current_location

    @property
    def questionnaire_store_updater(self):
        if not self._questionnaire_store_updater:
            self._questionnaire_store_updater = QuestionnaireStoreUpdater(
                self._current_location,
                self._schema,
                self._questionnaire_store,
                self.block.get('question'),
            )
        return self._questionnaire_store_updater

    @property
    def path_finder(self):
        if not self._path_finder:
            self._path_finder = PathFinder(
                self._schema,
                self._questionnaire_store.answer_store,
                self._questionnaire_store.metadata,
                self._questionnaire_store.progress_store,
                self._questionnaire_store.list_store,
            )
        return self._path_finder

    @property
    def placeholder_renderer(self):
        if not self._placeholder_renderer:
            self._placeholder_renderer = PlaceholderRenderer(
                self._language,
                schema=self._schema,
                answer_store=self._questionnaire_store.answer_store,
                metadata=self._questionnaire_store.metadata,
                location=self._current_location,
            )

        return self._placeholder_renderer

    @property
    def router(self):
        if not self._router:
            self._router = Router(
                self._schema,
                progress_store=self._questionnaire_store.progress_store,
                list_store=self._questionnaire_store.list_store,
            )
        return self._router

    def save_on_sign_out(self):
        self.questionnaire_store_updater.update_answers(self.form)
        # The location needs to be removed as we may have previously completed this location
        self.questionnaire_store_updater.remove_completed_location()
        self.questionnaire_store_updater.save()

    def is_location_valid(self):
        return self.router.can_access_location(
            self._current_location, self._routing_path
        )

    def get_previous_location_url(self):
        return self.router.get_previous_location_url(
            self._current_location, self._routing_path
        )

    def get_next_location_url(self):
        return self.router.get_next_location_url(
            self._current_location, self._routing_path
        )

    def handle_post(self):
        self.questionnaire_store_updater.add_completed_location()
        self._update_section_completeness()
        self.questionnaire_store_updater.save()

    def set_started_at_metadata(self):
        collection_metadata = self._questionnaire_store.collection_metadata
        if not collection_metadata.get('started_at'):
            started_at = datetime.utcnow().isoformat()

            logger.info(
                'Survey started. Writing started_at time to collection metadata',
                started_at=started_at,
            )

            collection_metadata['started_at'] = started_at

    def _get_routing_path(self):
        return self.path_finder.routing_path(
            section_id=self._current_location.section_id,
            list_item_id=self._current_location.list_item_id,
        )

    def _update_section_completeness(
        self, location: Optional[Location] = None, routing_path: Optional = None
    ):
        routing_path = routing_path if routing_path else self._routing_path
        section_status = (
            CompletionStatus.COMPLETED
            if self.path_finder.is_path_complete(routing_path)
            else CompletionStatus.IN_PROGRESS
        )

        location = location or self._current_location

        self.questionnaire_store_updater.update_section_status(
            section_status=section_status,
            section_id=location.section_id,
            list_item_id=location.list_item_id,
        )
