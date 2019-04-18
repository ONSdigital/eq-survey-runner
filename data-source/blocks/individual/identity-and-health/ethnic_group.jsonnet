local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description) = {
  id: 'ethnic-group-question',
  title: title,
  type: 'General',
  answers: [
    {
      guidance: {
        show_guidance: 'Why your answer is important',
        hide_guidance: 'Why your answer is important',
        content: [
          {
            description: 'Your answer will help to support equality and fairness in your community. Councils and government use information on ethnic group to make sure they:',
            list: [
              'provide services and share funding fairly',
              'understand and represent everyone’s interests',
            ],
          },
        ],
      },
      id: 'ethnic-group-answer',
      mandatory: true,
      options: [
        {
          label: 'White',
          value: 'White',
          description: description,
        },
        {
          label: 'Mixed or Multiple ethnic groups',
          value: 'Mixed or Multiple ethnic groups',
          description: 'Includes White and Black Caribbean, White and Black African, White and Asian or any other Mixed or Multiple background',
        },
        {
          label: 'Asian or Asian British',
          value: 'Asian or Asian British',
          description: 'Includes Indian, Pakistani, Bangladeshi, Chinese or any other Asian background',
        },
        {
          label: 'Black, Black British, Caribbean or African',
          value: 'Black, Black British, Caribbean or African',
          description: 'Includes Black British, Caribbean, African or any other Black background',
        },
        {
          label: 'Other ethnic group',
          value: 'Other ethnic group',
          description: 'Includes Arab or any other ethnic group',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'What is your ethnic group?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> ethnic group?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};
local englandDescription = 'Includes British, Northern Irish, Irish, Gypsy, Irish Traveller, Roma or any other White background';
local walesDescription = 'Includes Welsh, British, Northern Irish, Irish, Gypsy, Irish Traveller, Roma or any other White background';

{
  type: 'Question',
  id: 'ethnic-group',
  question_variants: [
    {
      question: question(nonProxyTitle, englandDescription),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, englandDescription),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, walesDescription),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, walesDescription),
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'white-ethnic-group',
        when: [
          {
            id: 'ethnic-group-answer',
            condition: 'equals',
            value: 'White',
          },
        ],
      },
    },
    {
      goto: {
        block: 'mixed-ethnic-group',
        when: [
          {
            id: 'ethnic-group-answer',
            condition: 'equals',
            value: 'Mixed or Multiple ethnic groups',
          },
        ],
      },
    },
    {
      goto: {
        block: 'asian-ethnic-group',
        when: [
          {
            id: 'ethnic-group-answer',
            condition: 'equals',
            value: 'Asian or Asian British',
          },
        ],
      },
    },
    {
      goto: {
        block: 'black-ethnic-group',
        when: [
          {
            id: 'ethnic-group-answer',
            condition: 'equals',
            value: 'Black, Black British, Caribbean or African',
          },
        ],
      },
    },
    {
      goto: {
        block: 'other-ethnic-group',
        when: [
          {
            id: 'ethnic-group-answer',
            condition: 'equals',
            value: 'Other ethnic group',
          },
        ],
      },
    },
    {
      goto: {
        block: 'religion',
      },
    },
  ],
}
