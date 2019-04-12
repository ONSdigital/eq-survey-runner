local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'employer-address-workplace-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'employer-address-workplace-answer-building',
      label: 'Building',
      mandatory: true,
      type: 'TextField',
    },
    {
      id: 'employer-address-workplace-answer-street',
      label: 'Street',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'employer-address-workplace-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'employer-address-workplace-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'employer-adress-workplace-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
      guidance: {
        show_guidance: 'Why your answer is important',
        hide_guidance: 'Why your answer is important',
        content: [
          {
            description: 'Workplace address and method of travel to work information is used to inform planning and modelling for transport services and policies. The information helps in the assessment of local public transport needs.',
          },
        ],
      },
    },
  ],
};

local nonProxyTitle = 'What is the address of your workplace?';
local proxyTitle = {
  text: 'What is the address of <em>{person_name_possessive}</em> workplace?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'employer-address-workplace',
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
  routing_rules: [
    {
      goto: {
        group: 'comments-group',
      },
    },
  ],
}
