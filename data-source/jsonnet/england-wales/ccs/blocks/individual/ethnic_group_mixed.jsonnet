local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'mixed-ethnic-group-question',
  title: title,
  type: 'General',
  answers: [
    {
      guidance: {
        show_guidance: 'Why your answer is important',
        hide_guidance: 'Why your answer is important',
        contents: [
          {
            description: 'Your answer will help to support equality and fairness in your community. Councils and government use information on ethnic group to make sure they',
            list: [
              'provide services and share funding fairly',
              'understand and represent everyone’s interests',
            ],
          },
        ],
      },
      id: 'mixed-ethnic-group-answer',
      mandatory: false,
      options: [
        {
          label: 'White and Black Caribbean',
          value: 'White and Black Caribbean',
        },
        {
          label: 'White and Black African',
          value: 'White and Black African',
        },
        {
          label: 'White and Asian',
          value: 'White and Asian',
        },
        {
          label: 'Any other Mixed or Multiple background',
          value: 'Other',
          description: 'Select to enter answer',
          detail_answer: {
            id: 'mixed-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Enter Mixed or Multiple background',
          },
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Which one best describes your Mixed or Multiple ethnic group or background?';
local proxyTitle = {
  text: 'Which one best describes <em>{person_name_possessive}</em> Mixed or Multiple ethnic group or background?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'mixed-ethnic-group',
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
        block: 'another-uk-address',
        when: [rules.under1],
      },
    },
    {
      goto: {
        block: 'another-uk-address',
        when: [rules.estimatedAgeUnder1],
      },
    },
    {
      goto: {
        block: 'past-usual-household-address',
        when: [rules.under4],
      },
    },
    {
      goto: {
        block: 'past-usual-household-address',
        when: [rules.estimatedAgeUnder4],
      },
    },
    {
      goto: {
        block: 'in-education',
      },
    },
  ],
}
