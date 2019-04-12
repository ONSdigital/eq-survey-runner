local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'length-of-stay-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'length-of-stay-answer',
      mandatory: true,
      options: [
        {
          label: 'Less than 12 months',
          value: 'Less than 12 months',
        },
        {
          label: '12 months or more',
          value: '12 months or more',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Including the time already spent here, how long do you intend to stay in the United Kingdom?';
local proxyTitle = {
  text: 'Including the time already spent here, how long does <em>{person_name}</em> intend to stay in the United Kingdom?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'length-of-stay',
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
  routing_rules: [
    {
      goto: {
        block: 'understand-welsh',
        when: [
          {
            meta: 'region_code',
            condition: 'equals',
            value: 'GB-WLS',
          },
        ],
      },
    },
    {
      goto: {
        block: 'language',
      },
    },
  ],
}
