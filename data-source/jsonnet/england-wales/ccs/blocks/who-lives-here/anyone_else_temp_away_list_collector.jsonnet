local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local summaryTitlePersonName = {
  text: '{person_name}',
  placeholders: [
    placeholders.personName,
  ],
};

local addPersonQuestionTitle = {
  text: 'Who do you need to add to {address}?',
  placeholders: [
    placeholders.address,
  ],
};

local primaryEditPersonQuestionTitle = {
  text: 'Change details for {person_name} (You)',
  placeholders: [
    placeholders.personName,
  ],
};

local nonPrimaryEditPersonQuestionTitle = {
  text: 'Change details for {person_name}',
  placeholders: [
    placeholders.personName,
  ],
};

local removePersonQuestionTitle = {
  text: 'Are you sure you want to remove {person_name}?',
  placeholders: [
    placeholders.personName,
  ],
};

local editQuestion(questionTitle) = {
  id: 'anyone-else-temp-away-edit-question',
  type: 'General',
  title: questionTitle,
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
};


{
  id: 'anyone-else-temp-away-list-collector',
  type: 'ListCollector',
  for_list: 'household',
  add_answer: {
    id: 'anyone-else-temp-away-answer',
    value: 'Yes',
  },
  remove_answer: {
    id: 'anyone-else-temp-away-remove-confirmation',
    value: 'Yes, I want to remove this person',
  },
  question: {
    id: 'anyone-else-temp-away-confirmation-question',
    type: 'General',
    title: 'Apart from the people already included, is there anyone else who was temporarily away or staying that you need to add?',
    guidance: {
      contents: [
        {
          description: 'Include',
        },
        {
          list: [
            'People from outside the UK who were staying in the UK for <strong>3 months or more</strong>',
            'Members of the armed forces',
            'Prisoners with a sentence of <strong>less than 12 months</strong>',
            'People expecting to stay in an establishment such as a hospital, care home or hostel for <strong>less than 6 months</strong>',
            'People who were temporarily outside the UK for <strong>less than 12 months</strong>',
            'People staying temporarily who did not have another UK address',
          ],
        },
      ],
    },
    answers: [
      {
        id: 'anyone-else-temp-away-answer',
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
  add_block: {
    id: 'anyone-else-temp-away-add-person',
    type: 'ListAddQuestion',
    question: {
      id: 'anyone-else-temp-away-add-question',
      type: 'General',
      title: addPersonQuestionTitle,
      description: '<em>Enter a full stop (.) if the respondent does not know a person\'s "First name" or "Last name"</em>',
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
  edit_block: {
    id: 'anyone-else-temp-away-edit-person',
    type: 'ListEditQuestion',
    question_variants: [
      {
        question: editQuestion(primaryEditPersonQuestionTitle),
        when: [rules.isPrimary],
      },
      {
        question: editQuestion(nonPrimaryEditPersonQuestionTitle),
        when: [rules.isNotPrimary],
      },
    ],
  },
  remove_block: {
    id: 'anyone-else-temp-away-remove-person',
    type: 'ListRemoveQuestion',
    question: {
      id: 'anyone-else-temp-away-remove-question',
      type: 'General',
      guidance: {
        contents: [{
          title: 'All of the data entered about this person will be deleted',
        }],
      },
      title: removePersonQuestionTitle,
      answers: [
        {
          id: 'anyone-else-temp-away-remove-confirmation',
          mandatory: true,
          type: 'Radio',
          options: [
            {
              label: 'Yes, I want to remove this person',
              value: 'Yes, I want to remove this person',
            },
            {
              label: 'No, I do not want to remove this person',
              value: 'No, I do not want to remove this person',
            },
          ],
        },
      ],
    },
  },
  summary: {
    title: 'Household members',
    item_title: summaryTitlePersonName,
    add_link_text: 'Add another visitor to this household',
    empty_list_text: 'There are no visitors',
  },
  show_on_section_summary: false,
}
