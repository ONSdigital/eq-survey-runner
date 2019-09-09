local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'when-arrive-in-uk-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'when-arrive-in-uk-answer',
      mandatory: false,
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
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Did you arrive in the UK, on or after 13 October 2018?';
local proxyTitle = {
  text: 'Did <em>{person_name}</em> arrive in the UK, on or after 13 October 2018?',
  placeholders: [
    placeholders.personName,
  ],
};

function(region_code) {
  type: 'Question',
  id: 'when-arrive-in-uk',
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
        block: 'length-of-stay',
        when: [
          {
            id: 'when-arrive-in-uk-answer',
            condition: 'equals',
            value: 'Yes',
          },
        ],
      },
    },
    {
      goto: {
        block: 'national-identity',
        when: [
          {
            id: 'when-arrive-in-uk-answer',
            condition: 'equals',
            value: 'No',
          },
          rules.under3,
        ],
      },
    },
    {
      goto: {
        block: if region_code == 'GB-WLS' then 'understand-welsh' else 'language',
        when: [
          {
            id: 'when-arrive-in-uk-answer',
            condition: 'equals',
            value: 'No',
          },
        ],
      },
    },
    {
      goto: {
        block: 'length-of-stay',
      },
    },
  ],
}
