local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'Have you achieved an NVQ or equivalent qualification?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved an NVQ or equivalent qualification?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'nvq-level-question',
  title: title,
  type: 'MutuallyExclusive',
  guidance: {
    contents: [
      {
        description: 'Include equivalent qualifications achieved anywhere outside Northern Ireland',
      },
    ],
  },
  mandatory: true,
  answers: [
    {
      id: 'nvq-level-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'NVQ level 3 or equivalent',
          value: 'NVQ level 3 or equivalent',
          description: 'For example BTEC National, OND or ONC, City and Guilds Advanced Craft',
        },
        {
          label: 'NVQ level 2 or equivalent',
          value: 'NVQ level 2 or equivalent',
          description: 'For example BTEC General, City and Guilds Craft',
        },
        {
          label: 'NVQ level 1 or equivalent',
          value: 'NVQ level 1 or equivalent',
        },
      ],
    },
    {
      id: 'nvq-level-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'None of these apply',
          value: 'None of these apply',
          description: 'Questions on A levels, GCSEs and equivalents will follow',
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'nvq-level',
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
