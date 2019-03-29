local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'asian-ethnic-group-question',
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
      id: 'asian-ethnic-group-answer',
      mandatory: true,
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
          detail_answer: {
            id: 'asian-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify Asian background',
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
