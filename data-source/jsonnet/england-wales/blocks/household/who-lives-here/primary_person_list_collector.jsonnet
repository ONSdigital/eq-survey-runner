local placeholders = import '../../../lib/placeholders.libsonnet';

local questionTitle = {
  text: 'Do you usually live at {address}?',
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
    value: 'Yes, I usually live here',
  },
  add_or_edit_block: {
    id: 'add-or-edit-primary-person',
    type: 'PrimaryPersonListAddOrEditQuestion',
    question: {
      id: 'primary-person-add-or-edit-question',
      type: 'General',
      title: 'What is your name?',
      answers: [
        {
          id: 'first-name',
          label: 'First name',
          mandatory: true,
          type: 'TextField',
        },
        {
          id: 'middle-names',
          label: 'Middle names',
          mandatory: false,
          type: 'TextField',
        },
        {
          id: 'last-name',
          label: 'Last name',
          mandatory: true,
          type: 'TextField',
        },
      ],
    },
  },
  question: {
    id: 'primary-confirmation-question',
    type: 'General',
    title: questionTitle,
    definitions: [
      {
        title: 'What does "usually live" mean?',
        contents: [
          {
            description: 'It means the address at which you generally spend most time. For most people, this will be their permanent or family home.',
          },
          {
            description: '<strong>Full-time students</strong>, include yourself at your term time address.',
          },
          {
            description: '<strong>Armed forces members</strong>, include yourself at your home address if you have one.',
          },
        ],
      },
    ],
    answers: [
      {
        id: 'you-live-here-answer',
        mandatory: true,
        type: 'Radio',
        options: [
          {
            label: 'Yes, I usually live here',
            value: 'Yes, I usually live here',
          },
          {
            label: 'No, I don’t usually live here',
            value: 'No, I don’t usually live here',
          },
        ],
      },
    ],
  },
}
