local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'last-year-address-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'last-year-address-answer-building',
      label: 'House name or number',
      mandatory: true,
      type: 'TextField',
    },
    {
      id: 'last-year-address-answer-street',
      label: 'Street',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'last-year-address-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'last-year-address-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'last-year-address-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitle = 'Enter details of your address one year ago';
local proxyTitle = 'Enter details of their address one year ago';

{
  type: 'Question',
  id: 'last-year-address',
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
