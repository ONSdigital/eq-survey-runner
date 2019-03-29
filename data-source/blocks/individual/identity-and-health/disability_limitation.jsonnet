local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'disability-limitation-question',
  title: title,
  definitions: [
    {
      title: 'What do we mean by reduce your ability?',
      content: [
        {
          description: 'This question is asking whether your health condition or illness currently affects your ability to carry-out normal daily activities.',
        },
        {
          description: 'You should consider whether you are still affected whilst receiving any treatment, medication or using any devices for your condition or illness. For example, if you require a hearing aid and by using the device, you experience no restriction in carrying out your day-to-day activities, then you should select ‘Not at all’.',
        },
        {
          description: '‘Yes, a lot’, should be selected if you usually need some level of support of family members, friends or personal social services for most normal daily activities.',
        },
      ],
    },
  ],
  type: 'General',
  answers: [
    {
      id: 'disability-limitation-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes, a lot',
          value: 'Yes, a lot',
        },
        {
          label: 'Yes, a little',
          value: 'Yes, a little',
        },
        {
          label: 'Not at all',
          value: 'Not at all',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Do any of your conditions or illnesses reduce your ability to carry out day-to-day activities?';
local proxyTitle = {
  text: 'Does any of <em>{person_name_possessive}</em> conditions or illnesses reduce their ability to carry out day-to-day activities?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'disability-limitation',
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
}
