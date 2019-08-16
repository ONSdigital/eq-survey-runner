local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description) = {
  title: title,
  id: 'work_location_type-question',
  description: description,
  type: 'General',
  answers: [
    {
      id: 'work_location_type-answer',
      mandatory: true,
      options: [
        {
          label: 'At a workplace',
          value: 'At a workplace',
        },
        {
          label: 'At or from home',
          value: 'At or from home',
        },
        {
          label: 'No fixed place',
          value: 'No fixed place',
        },
      ],
      type: 'Radio',
    },
  ],
};


local nonProxyTitleWork = 'Where do you mainly work?';
local proxyTitleWork = {
  text: 'Where does <em>{person_name}</em> mainly work?',
  placeholders: [
    placeholders.personName,
  ],
};
local nonProxyTitleDidWork = 'Where did you mainly work?';
local proxyTitleDidWork = {
  text: 'Where did <em>{person_name}</em> mainly work?',
  placeholders: [
    placeholders.personName,
  ],
};

local nonProxyDescriptionWork = 'Answer for the place where you spend the most time. Even if ill, on maternity leave, holiday or temporarily laid off provide details of your main place of work.';
local proxyDescriptionWork = 'Answer for the place where <em>{person_name}</em> spends the most time. Even if ill, on maternity leave, holiday or temporarily laid off provide details of their main place of work.';
local nonProxyDescriptionDidWork = 'Answer for the place where you spent the most time.';
local proxyDescriptionDidWork = 'Answer for the place where <em>{person_name}</em> spent the most time.';

{
  type: 'Question',
  id: 'work_location_type',
  question_variants: [
    {
      question: question(nonProxyTitleWork, nonProxyDescriptionWork),
      when: [rules.proxyNo, rules.mainJob],
    },
    {
      question: question(proxyTitleWork, proxyDescriptionWork),
      when: [rules.proxyYes, rules.mainJob],
    },
    {
      question: question(nonProxyTitleDidWork, nonProxyDescriptionDidWork),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitleDidWork, proxyDescriptionDidWork),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'work-location',
        when: [
          {
            id: 'work_location_type-answer',
            condition: 'equals',
            value: 'At a workplace',
          },
        ],
      },
    },
    {
      goto: {
        group:'submit-group',
      },
    },
  ],
}