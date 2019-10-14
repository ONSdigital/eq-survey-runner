local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, options) = {
  id: 'term-time-location-question',
  type: 'General',
  title: title,
  answers: [
    {
      id: 'term-time-location-answer',
      mandatory: false,
      type: 'Radio',
    } + options,
  ],
};

local nonProxyTitle = 'During term time, where did you usually live?';
local proxyTitle = {
  text: 'During term time, where did <em>{person_name}</em> usually live?',
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
      label: 'At another address',
      value: 'At another address',
    },
  ],
};

{
  type: 'Question',
  id: 'term-time-location',
  question_variants: [
    {
      question: question(nonProxyTitle, noOtherAddressOptions),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, noOtherAddressOptions),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'another-uk-address',
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
        block: 'past-usual-household-address',
      },
    },
  ],
}
