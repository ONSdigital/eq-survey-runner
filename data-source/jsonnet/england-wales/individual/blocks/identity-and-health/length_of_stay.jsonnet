local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'length-of-stay-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'length-of-stay-answer',
      mandatory: false,
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

function(region_code) {
  type: 'Question',
  id: 'length-of-stay',
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
  routing_rules: [
    {
      goto: {
        block: 'national-identity',
        when: [
          rules.under3,
        ],
      },
    },
    {
      goto: {
        block: if region_code == 'GB-WLS' then 'understand-welsh' else 'language',
      },
    },
  ],
}
