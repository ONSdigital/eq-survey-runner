local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'work-location-question',
  type: 'General',
  title: title,
  answers: [
    {
      id: 'work-address-details-answer-building',
      label: 'Address line 1',
      mandatory: true,
      type: 'TextField',
    },
    {
      id: 'work-address-details-answer-street',
      label: 'Address line 2',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'work-address-details-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'work-address-details-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'work-address-details-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitleWork = 'What is the address of your main place of work?';
local proxyTitleWork = {
  text: 'What is the address of <em>{person_name_possessive}</em> main place of work?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local pastNonProxyTitleWork = 'What was the address of your main place of work?';
local pastProxyTitleWork = {
  text: 'What was the address of <em>{person_name_possessive}</em> main place of work?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};


{
  type: 'Question',
  id: 'work-location',
  question_variants: [
    {
      question: question(nonProxyTitleWork),
      when: [rules.isNotProxy, rules.mainJob],
    },
    {
      question: question(proxyTitleWork),
      when: [rules.isProxy, rules.mainJob],
    },
    {
      question: question(pastNonProxyTitleWork),
      when: [rules.isNotProxy],
    },
    {
      question: question(pastProxyTitleWork),
      when: [rules.isProxy],
    },
  ],
}
