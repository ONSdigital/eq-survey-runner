local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, description) = {
  id: 'past-usual-address-household-question',
  title: title,
  type: 'General',
  description: description,
  answers: [
    {
      id: 'past-usual-address-household-answer',
      mandatory: false,
      options: [
        {
          label: {
            text: '{address}',
            placeholders: [
              placeholders.address,
            ],
          },
          value: 'household-address',
        },
        {
          label: 'Another address in the UK',
          value: 'Another address in the UK',
        },
        {
          label: 'An address outside the UK',
          value: 'Other',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'One year ago, on 13 October 2019 what was your usual address?';
local nonProxyDescription = 'If you had no usual address one year ago, state the address where you were staying';
local proxyTitle = {
  text: 'One year ago, on 13 October 2019, what was <em>{person_name_possessive}</em> usual address?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};
local proxyDescription = 'If they had no usual address one year ago, state the address where they were staying';

{
  type: 'Question',
  id: 'past-usual-household-address',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDescription),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, proxyDescription),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'another-uk-address',
        when: [
          {
            id: 'past-usual-address-household-answer',
            condition: 'not equals',
            value: 'Other',
          },
          rules.under16,
        ],
      },
    },
    {
      goto: {
        block: 'employment-status',
        when: [
          {
            id: 'past-usual-address-household-answer',
            condition: 'not equals',
            value: 'Other',
          },
          rules.over16,
        ],
      },
    },
    {
      goto: {
        block: 'employment-status',
        when: [
          {
            id: 'past-usual-address-household-answer',
            condition: 'not equals',
            value: 'Other',
          },
          rules.estimatedAge,
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
