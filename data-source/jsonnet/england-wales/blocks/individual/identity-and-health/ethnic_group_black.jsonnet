local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'black-ethnic-group-question',
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
      id: 'black-ethnic-group-answer',
      mandatory: false,
      options: [
        {
          label: 'Caribbean',
          value: 'Caribbean',
        },
        {
          label: 'African',
          value: 'African',
          description: 'Select to enter answer',
          detail_answer: {
            id: 'african-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Enter African background',
          },
        },
        {
          label: 'Any other Black, Black British or Caribbean background',
          value: 'Other',
          description: 'Select to enter answer',
          detail_answer: {
            id: 'black-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Enter Black, Black British or Caribbean background',
          },
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Which one best describes your Black, Black British, Caribbean or African ethnic group or background?';
local proxyTitle = {
  text: 'Which one best describes <em>{person_name_possessive}</em> Black, Black British, Caribbean or African ethnic group or background?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'black-ethnic-group',
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
        block: 'religion',
      },
    },
  ],
}
