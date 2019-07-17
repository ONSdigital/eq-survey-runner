from typing import List, Mapping, Union

from flask import url_for
from flask_babel import lazy_gettext

from app.data_model.progress_store import CompletionStatus, ProgressStore


class HubContext:
    HUB_CONTENT_STATES = {
        'COMPLETE': {
            'title': lazy_gettext('Submit survey'),
            'description': lazy_gettext('Please submit this survey to complete it'),
            'submit_button': lazy_gettext('Submit survey'),
        },
        'INCOMPLETE': {
            'title': lazy_gettext('Choose another section to complete'),
            'description': lazy_gettext(
                'You must complete all sections in order to submit this survey'
            ),
            'submit_button': lazy_gettext('Continue'),
        },
    }

    SECTION_CONTENT_STATES = {
        CompletionStatus.COMPLETED: {
            'text': lazy_gettext('Completed'),
            'link': {
                'text': lazy_gettext('View answers'),
                'aria_label': lazy_gettext('View answers for {section_name}'),
            },
        },
        CompletionStatus.IN_PROGRESS: {
            'text': lazy_gettext('Partially completed'),
            'link': {
                'text': lazy_gettext('Continue with section'),
                'aria_label': lazy_gettext('Continue with {section_name} section'),
            },
        },
        CompletionStatus.NOT_STARTED: {
            'text': lazy_gettext('Not started'),
            'link': {
                'text': lazy_gettext('Start section'),
                'aria_label': lazy_gettext('Start {section_name} section'),
            },
        },
    }

    def __init__(
        self, progress_store: ProgressStore, sections: Mapping, survey_complete: bool
    ) -> None:
        self._progress_store = progress_store
        self._sections = sections
        self._survey_complete = survey_complete

    def get_context(self) -> Mapping:
        context = self.HUB_CONTENT_STATES[
            'COMPLETE' if self._survey_complete else 'INCOMPLETE'
        ]
        context['rows'] = self._get_rows()

        return context

    @staticmethod
    def get_section_url(section_id: str) -> str:
        return url_for('questionnaire.get_section', section_id=section_id)

    def get_row_for_section(
        self, section_name: str, section_status: str, section_url: str
    ) -> Mapping[str, Union[str, List]]:

        section_content = self.SECTION_CONTENT_STATES[section_status]

        context: Mapping = {
            'title': section_name,
            'rowItems': [
                {
                    'valueList': [{'text': section_content['text']}],
                    'actions': [
                        {
                            'text': section_content['link']['text'],
                            'ariaLabel': section_content['link']['aria_label'].format(
                                section_name=section_name
                            ),
                            'url': section_url,
                        }
                    ],
                }
            ],
        }

        if section_status == CompletionStatus.COMPLETED:
            context['rowItems'][0]['icon'] = 'check-green'

        return context

    def _get_rows(self) -> List[Mapping[str, Union[str, List]]]:
        rows = []

        for section in self._sections:
            section_status = self._progress_store.get_section_status(section['id'])

            section_name = section['title']
            section_url = self.get_section_url(section['id'])

            rows.append(
                self.get_row_for_section(section_name, section_status, section_url)
            )

        return rows
