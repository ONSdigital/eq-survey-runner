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
        content: [
          {
            description: 'How you define your ethnic group is up to you. Sharing this information enables the government and other organisations to provide appropriate resources and policies such as housing, education, health and criminal justice.',
          },
        ],
      },
      id: 'black-ethnic-group-answer',
      mandatory: true,
      options: [
        {
          label: 'Caribbean',
          value: 'Caribbean',
        },
        {
          label: 'African',
          value: 'African',
          detail_answer: {
            id: 'african-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify African background',
          },
        },
        {
          label: 'Any Black, Black British or Caribbean background',
          value: 'Other',
          detail_answer: {
            id: 'black-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify Black, Black British, or Caribbean background',
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
