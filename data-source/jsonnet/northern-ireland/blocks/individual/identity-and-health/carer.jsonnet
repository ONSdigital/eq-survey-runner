local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title, guidance) = {
  id: 'carer-question',
  title: title,
  guidance: {
    contents: [
      {
        description: guidance,
      },
    ],
  },
  type: 'General',
  answers: [
    {
      id: 'carer-answer',
      mandatory: true,
      options: [
        {
          label: 'No',
          value: 'No',
        },
        {
          label: 'Yes, 19 hours or less a week',
          value: 'Yes, 19 hours or less a week',
        },
        {
          label: 'Yes, 20 to 34 hours a week',
          value: 'Yes, 20 to 34 hours a week',
        },
        {
          label: 'Yes, 35 to 49 hours a week',
          value: 'Yes, 35 to 49 hours a week',
        },
        {
          label: 'Yes, 50 hours or more a week',
          value: 'Yes, 50 hours or more a week',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Do you look after, or give any help or support to, anyone because they have long-term physical or mental health conditions or illnesses, or problems related to old age?';
local nonProxyGuidance = 'Exclude anything you do in paid employment';
local proxyTitle = {
  text: 'Does <em>{person_name}</em> look after, or give any help or support to, anyone because they have long-term physical or mental health conditions or illnesses, or problems related to old age?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyGuidance = 'Exclude anything they do in paid employment';

{
  type: 'Question',
  id: 'carer',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyGuidance),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyGuidance),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'sexual-identity',
        when: [
          rules.over16,
        ],
      },
    },
    {
      goto: {
        group: 'school-group',
      },
    },
  ],
}
