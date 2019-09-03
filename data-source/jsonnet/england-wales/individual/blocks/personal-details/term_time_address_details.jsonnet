local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'term-time-address-details-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'term-time-address-details-answer-building',
      label: 'Address line 1',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'term-time-address-details-answer-street',
      label: 'Address line 2',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'term-time-address-details-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'term-time-address-details-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'term-time-address-details-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitle = 'Enter details of the UK address where you usually stay during term time.';
local proxyTitle = {
  text: 'Enter details of the UK address where <em>{person_name}</em> usually stays during term time.',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'term-time-address-details',
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
        group: 'submit-group',
      },
    },
  ],
}
