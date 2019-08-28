local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'school-location-question',
  type: 'General',
  title: title,
  answers: [
    {
      id: 'school-address-details-answer-building',
      label: 'Address line 1',
      mandatory: true,
      type: 'TextField',
    },
    {
      id: 'school-address-details-answer-street',
      label: 'Address line 2',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'school-address-details-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'school-address-details-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'school-address-details-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitleSchool = 'What is the address of your main place of study, including school?';
local proxyTitleSchool = {
  text: 'What is the address of <em>{person_name_possessive}</em> main place of study, including school?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'school-location',
  question_variants: [
    {
      question: question(nonProxyTitleSchool),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitleSchool),
      when: [rules.isProxy],
    },
  ],
}
