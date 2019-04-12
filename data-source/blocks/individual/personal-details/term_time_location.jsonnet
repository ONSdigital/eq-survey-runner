local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, options) = {
  id: 'term-time-location-question',
  type: 'General',
  title: title,
  answers: [
    {
      id: 'term-time-location-answer',
      mandatory: true,
      type: 'Radio',
    } + options,
  ],
};

local nonProxyTitle = 'During term time, where do you usually live?';
local proxyTitle = {
  text: 'During term time, where does <em>{person_name}</em> usually live?',
  placeholders: [
    placeholders.personName,
  ],
};

local noOtherAddressOptions = {
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
      label: 'Another address',
      value: 'Another address',
    },
  ],
};

local otherUkAddressOptions = {
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
      label: {
        text: '{address}',
        placeholders: [
          {
            placeholder: 'address',
            transforms: [{
              transform: 'concatenate_list',
              arguments: {
                list_to_concatenate: {
                  source: 'answers',
                  identifier: ['other-address-answer-building', 'other-address-answer-street'],
                },
                delimiter: ', ',
              },
            }],
          },
        ],
      },
      value: '30-day-address',
    },
    {
      label: 'Another address',
      value: 'Another address',
    },
  ],
};

local otherNonUkAddressOptions = {
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
      label: {
        text: 'The address in {country}',
        placeholders: [
          {
            placeholder: 'country',
            value: {
              source: 'answers',
              identifier: 'another-address-answer-other-country',
            },
          },
        ],
      },
      value: '30-day-address',
    },
    {
      label: 'Another address',
      value: 'Another address',
    },
  ],
};

{
  type: 'Question',
  id: 'term-time-location',
  question_variants: [
    {
      question: question(nonProxyTitle, otherNonUkAddressOptions),
      when: [
        rules.proxyNo,
        {
          id: 'another-address-answer',
          condition: 'equals',
          value: 'Other',
        },
      ],
    },
    {
      question: question(proxyTitle, otherNonUkAddressOptions),
      when: [
        rules.proxyYes,
        {
          id: 'another-address-answer',
          condition: 'equals',
          value: 'Other',
        },
      ],
    },
    {
      question: question(nonProxyTitle, otherUkAddressOptions),
      when: [
        rules.proxyNo,
        {
          id: 'another-address-answer',
          condition: 'equals',
          value: 'Yes, an address within the UK',
        },
      ],
    },
    {
      question: question(proxyTitle, otherUkAddressOptions),
      when: [
        rules.proxyYes,
        {
          id: 'another-address-answer',
          condition: 'equals',
          value: 'Yes, an address within the UK',
        },
      ],
    },
    {
      question: question(nonProxyTitle, noOtherAddressOptions),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, noOtherAddressOptions),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'term-time-address-country',
        when: [
          {
            id: 'another-address-answer',
            condition: 'equals',
            value: 'No',
          },
          {
            id: 'term-time-location-answer',
            condition: 'equals',
            value: 'Another address',
          },
        ],
      },
    },
    {
      goto: {
        group: 'comments-group',
        when: [
          {
            id: 'term-time-location-answer',
            condition: 'equals',
            value: 'Another address',
          },
        ],
      },
    },
    {
      goto: {
        group: 'comments-group',
        when: [
          {
            id: 'term-time-location-answer',
            condition: 'equals',
            value: '30-day-address',
          },
        ],
      },
    },
    {
      goto: {
        group: 'identity-and-health-group',
      },
    },
  ],
}
