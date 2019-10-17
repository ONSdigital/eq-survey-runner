local placeholders = import '../../../lib/placeholders.libsonnet';

local questionTitle = {
  text: 'Were you usually living at {address} on Sunday 13 October 2019?',
  placeholders: [
    placeholders.address,
  ],
};

{
  id: 'primary-person-list-collector',
  type: 'PrimaryPersonListCollector',
  for_list: 'household',
  add_or_edit_answer: {
    id: 'you-live-here-answer',
    value: 'Yes',
  },
  add_or_edit_block: {
    id: 'add-or-edit-primary-person',
    type: 'PrimaryPersonListAddOrEditQuestion',
    question: {
      id: 'primary-person-add-or-edit-question',
      type: 'General',
      title: 'What is your full name?',
      answers: [
        {
          id: 'first-name',
          label: 'First name',
          mandatory: true,
          autocomplete: 'given-name',
          type: 'TextField',
        },
        {
          id: 'middle-names',
          label: 'Middle names',
          mandatory: false,
          autocomplete: 'additional-name',
          type: 'TextField',
        },
        {
          id: 'last-name',
          label: 'Last name',
          mandatory: true,
          autocomplete: 'family-name',
          type: 'TextField',
        },
      ],
    },
  },
  question: {
    id: 'primary-confirmation-question',
    type: 'General',
    title: questionTitle,
    description: '<em>Tell respondent to turn to <strong>Showcard 1</strong></em>',
    answers: [
      {
        id: 'you-live-here-answer',
        mandatory: true,
        type: 'Radio',
        options: [
          {
            label: 'Yes',
            value: 'Yes',
          },
          {
            label: 'No',
            value: 'No',
          },
        ],
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'anyone-else-usually-living',
        when: [
          {
            id: 'you-live-here-answer',
            condition: 'equals',
            value: 'No',
          },
        ],
      },
    },
    {
      goto: {
        block: 'anyone-else-list-collector',
      },
    },
  ],
}
