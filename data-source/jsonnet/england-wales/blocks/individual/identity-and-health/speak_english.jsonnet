local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title) = {
  id: 'english-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'english-answer',
      mandatory: false,
      options: [
        {
          label: 'Very well',
          value: 'Very well',
        },
        {
          label: 'Well',
          value: 'Well',
        },
        {
          label: 'Not well',
          value: 'Not well',
        },
        {
          label: 'Not at all',
          value: 'Not at all',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'How well can you speak English?';
local proxyTitle = {
  text: 'How well can <em>{person_name}</em> speak English?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'english',
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
