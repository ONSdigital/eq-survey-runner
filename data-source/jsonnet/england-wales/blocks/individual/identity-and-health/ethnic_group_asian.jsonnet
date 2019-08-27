local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'asian-ethnic-group-question',
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
      id: 'asian-ethnic-group-answer',
      mandatory: false,
      options: [
        {
          label: 'Indian',
          value: 'Indian',
        },
        {
          label: 'Pakistani',
          value: 'Pakistani',
        },
        {
          label: 'Bangladeshi',
          value: 'Bangladeshi',
        },
        {
          label: 'Chinese',
          value: 'Chinese',
        },
        {
          label: 'Any other Asian background',
          value: 'Other',
          description: 'Select to enter answer',
          detail_answer: {
            id: 'asian-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Enter Asian background',
          },
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Which one best describes your Asian or Asian British ethnic group or background?';
local proxyTitle = {
  text: 'Which one best describes <em>{person_name_possessive}</em> Asian or Asian British ethnic group or background?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'asian-ethnic-group',
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
        block: 'religion',
      },
    },
  ],
}
