local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local questionTitle = {
  text: 'Did anyone usually live at {address} on Sunday 13 October 2019?',
  placeholders: [
    placeholders.address,
  ],
};

local questionVariantTitle = {
  text: 'Did anyone else usually live at {address} on Sunday 13 October 2019?',
  placeholders: [
    placeholders.address,
  ],
};

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
  id: 'edit-question',
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

function(census_date) {
  id: 'anyone-else-list-collector',
  type: 'ListCollector',
  for_list: 'household',
  add_answer: {
    id: 'anyone-else-answer',
    value: 'Yes',
  },
  remove_answer: {
    id: 'remove-confirmation',
    value: 'Yes, I want to remove this person',
  },
  question_variants: [
    {
      question: {
        type: 'General',
        id: 'anyone-usually-live-at-question',
        title: questionTitle,
        guidance: {
          contents: [
            {
              description: 'Remember to only include those people who share cooking facilities and share a living room or sitting room or dining area',
            },
          ],
        },
        description: 'Tell respondent to turn to <strong>Showcard 2</strong>',
        answers: [
          {
            id: 'anyone-else-answer',
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
      when: [rules.listIsEmpty('household')],
    },
    {
      question: {
        id: 'anyone-usually-live-at-question',
        type: 'General',
        title: questionVariantTitle,
        guidance: {
          contents: [
            {
              description: 'Remember to only include those people who share cooking facilities and share a living room or sitting room or dining area',
            },
          ],
        },
        description: '<em>Tell respondent to turn to <strong>Showcard 2</strong></em>',
        answers: [
          {
            id: 'anyone-else-answer',
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
      when: [rules.listIsNotEmpty('household')],
    },
  ],
  add_block: {
    id: 'add-person',
    type: 'ListAddQuestion',
    question: {
      id: 'add-question',
      type: 'General',
      title: addPersonQuestionTitle,
      description: '<em>Enter a full stop (.) if the respondent does not know a person’s “First name” or “Last name”</em>',
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
    id: 'edit-person',
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
    id: 'remove-person',
    type: 'ListRemoveQuestion',
    question: {
      id: 'remove-question',
      type: 'General',
      guidance: {
        contents: [{
          title: 'All of the data entered about this person will be deleted',
        }],
      },
      title: removePersonQuestionTitle,
      answers: [
        {
          id: 'remove-confirmation',
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
    add_link_text: 'Add someone to this household',
    empty_list_text: 'There are no householders',
  },
}
