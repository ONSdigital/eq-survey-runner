local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, definitionContent) = {
  id: 'disability-question',
  title: title,
  definitions: [
    {
      title: 'What do we mean by “physical and mental health conditions or illnesses”?',
      contents: definitionContent,
    },
  ],
  type: 'General',
  answers: [
    {
      id: 'disability-answer',
      mandatory: false,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No',
          value: 'No',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Do you have any physical or mental health conditions or illnesses lasting or expected to last 12 months or more?';
local nonProxyDefinitionContent = [
  {
    description: 'This refers to health conditions, illnesses or impairments you may have.',
  },
  {
    description: 'Consider conditions that always affect you and those that flare up from time to time. These may include, for example, sensory conditions, developmental conditions or learning impairments.',
  },
];
local proxyTitle = {
  text: 'Does <em>{person_name}</em> have any physical or mental health conditions or illnesses lasting or expected to last 12 months or more?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyDefinitionContent = [
  {
    description: 'This refers to health conditions, illnesses or impairments they may have.',
  },
  {
    description: 'Consider conditions that always affect them and those that flare up from time to time. These may include, for example, sensory conditions, developmental conditions or learning impairments.',
  },
];

{
  type: 'Question',
  id: 'disability',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDefinitionContent),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, proxyDefinitionContent),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'disability-limitation',
        when: [
          {
            id: 'disability-answer',
            condition: 'equals',
            value: 'Yes',
          },
        ],
      },
    },
    {
      goto: {
        group: 'submit-group',
        when: [
          {
            id: 'disability-answer',
            condition: 'equals',
            value: 'No',
          },
          rules.under5,
        ],
      },
    },
    {
      goto: {
        group: 'submit-group',
        when: [
          {
            id: 'disability-answer',
            condition: 'not set',
          },
          rules.under5,
        ],
      },
    },
    {
      goto: {
        block: 'carer',
      },
    },
  ],
}
