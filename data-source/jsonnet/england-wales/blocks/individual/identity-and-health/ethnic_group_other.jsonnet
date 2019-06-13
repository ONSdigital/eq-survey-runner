local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title) = {
  id: 'other-ethnic-group-question',
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
      id: 'other-ethnic-group-answer',
      mandatory: true,
      options: [
        {
          label: 'Arab',
          value: 'Arab',
        },
        {
          label: 'Any other ethnic group',
          value: 'Other',
          detail_answer: {
            id: 'other-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify other ethnic group',
          },
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Which one best describes your other ethnic group or background?';
local proxyTitle = {
  text: 'Which one best describes <em>{person_name_possessive}</em> other ethnic group or background?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'other-ethnic-group',
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
