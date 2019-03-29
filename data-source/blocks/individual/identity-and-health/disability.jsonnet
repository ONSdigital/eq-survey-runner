local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'disability-question',
  title: title,
  definitions: [
    {
      title: 'What do we mean by physical and mental health conditions or illness?',
      content: [
        {
          description: 'Physical and mental health conditions or illnesses may also be described as disabilities.',
        },
        {
          description: 'For example sensory impairments such as sight or hearing loss, developmental conditions such as autism or Asperger’s syndrome, and learning impairment such as Down’s syndrome or dyslexia.',
        },
      ],
    },
  ],
  type: 'General',
  answers: [
    {
      id: 'disability-answer',
      mandatory: true,
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
local proxyTitle = {
  text: 'Does <em>{person_name}</em> have any physical or mental health conditions or illnesses lasting or expected to last 12 months or more?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'disability',
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
        block: 'carer',
      },
    },
  ],
}
