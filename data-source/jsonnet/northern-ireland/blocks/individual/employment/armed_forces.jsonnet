local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'armed-forces-question',
  title: title,
  guidance: {
    contents: [
      {
        description: 'Current serving members should only select “No”',
      },
    ],
  },
  type: 'General',
  answers: [
    {
      id: 'armed-forces-answer',
      mandatory: false,
      label: '',
      options: [
        {
          label: 'No',
          value: 'No',
        },
        {
          label: 'Yes, previously served in Regular Armed Forces',
          value: 'Yes, previously served in Regular Armed Forces',
        },
        {
          label: 'Yes, previously served in Reserve Armed Forces',
          value: 'Yes, previously served in Reserve Armed Forces',
        },
      ],
      type: 'Checkbox',
    },
  ],
};

local nonProxyTitle = 'Have you <em>previously</em> served in the UK Armed Forces?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> <em>previously</em> served in the UK Armed Forces?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'armed-forces',
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
