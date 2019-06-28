from typing import List, Mapping, Union

from flask import url_for
from flask_babel import lazy_gettext as _

from app.data_model.progress_store import CompletionStatus, ProgressStore


class HubContext:
    HUB_CONTENT_STATES = {
        'COMPLETE': {
            'title': _('Submit survey'),
            'description': _('Please submit this survey to complete it'),
            'submit_button': _('Submit survey'),
        },
        'INCOMPLETE': {
            'title': _('Choose another section to complete'),
            'description': _(
                'You must complete all sections in order to submit this survey'
            ),
            'submit_button': _('Continue'),
        },
    }

    SECTION_CONTENT_STATES = {
        CompletionStatus.COMPLETED: {
            'text': _('Completed'),
            'link': {
                'text': _('View answers'),
                'aria_label': _('View answers for {section_name}'),
            },
        },
        CompletionStatus.IN_PROGRESS: {
            'text': _('Partially completed'),
            'link': {
                'text': _('Continue with section'),
                'aria_label': _('Continue with {section_name} section'),
            },
        },
        CompletionStatus.NOT_STARTED: {
            'text': _('Not started'),
            'link': {
                'text': _('Start section'),
                'aria_label': _('Start {section_name} section'),
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
        return url_for('questionnaire.get_hub_section', section_id=section_id)

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
