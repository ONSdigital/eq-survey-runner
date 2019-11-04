local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'other-census-address-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'other-census-address-answer-building',
      label: 'Address line 1',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'other-census-address-answer-street',
      label: 'Address line 2',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'other-census-address-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'other-census-address-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'other-census-address-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitle = 'What is the other address where you may have been included on a Census questionnaire?';

local proxyTitle = {
  text: 'What is the other address where {person_name} may have been included on a Census questionnaire?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'other-census-address',
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
}
