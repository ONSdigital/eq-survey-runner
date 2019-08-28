local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'birth-gender-question',
  title: title,
  type: 'General',
  guidance: {
    contents: [
      {
        description: 'This question is <strong>voluntary</strong>',
      },
    ],
  },
  answers: [
    {
      id: 'birth-gender-answer',
      mandatory: false,
      label: '',
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No',
          value: 'No',
          description: 'An option to enter gender will follow',
          detail_answer: {
            id: 'birth-gender-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Enter gender',
          },
        },
      ],
      type: 'Checkbox',
    },
  ],
};

local nonProxyTitle = 'Is your gender the same as the sex you were registered at birth?';
local proxyTitle = {
  text: 'Is <em>{person_name_possessive}</em> gender the same as the sex they were registered at birth?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'birth-gender',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
  ],
}
