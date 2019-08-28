local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'frequency-irish-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'frequency-irish-answer',
      mandatory: false,
      type: 'Radio',
      options: [
        {
          label: 'Daily',
          value: 'Daily',
        },
        {
          label: 'Weekly',
          value: 'Weekly',
        },
        {
          label: 'Less often',
          value: 'Less often',
        },
        {
          label: 'Never',
          value: 'Never',
        },
      ],
    },
  ],
};

local nonProxyTitle = 'How often do you speak Irish?';
local proxyTitle = {
  text: 'How often does <em>{person_name}</em> speak Irish?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'frequency-irish',
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
