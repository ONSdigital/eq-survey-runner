local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'birth-gender-question',
  title: title,
  type: 'General',
  description: 'This question is voluntary',
  answers: [
    {
      id: 'birth-gender-answer',
      mandatory: true,
      label: 'Select one option only',
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No',
          value: 'No',
          detail_answer: {
            id: 'birth-gender-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify gender',
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
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle),
      when: [rules.proxyYes],
    },
  ],
}
