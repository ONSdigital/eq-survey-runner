local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'understand-welsh-question',
  title: title,
  guidance: {
    content: [
      {
        title: 'A question about national identity, including Welsh, will follow',
      },
    ],
  },
  mandatory: true,
  type: 'MutuallyExclusive',
  answers: [
    {
      id: 'understand-welsh-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'Understand spoken Welsh',
          value: 'Understand spoken Welsh',
        },
        {
          label: 'Speak Welsh',
          value: 'Speak Welsh',
        },
        {
          label: 'Read Welsh',
          value: 'Read Welsh',
        },
        {
          label: 'Write Welsh',
          value: 'Write Welsh',
        },
      ],
    },
    {
      id: 'understand-welsh-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'None of the these',
          value: 'None of the these',
        },
      ],
    },
  ],
};

local nonProxyTitle = 'Can you understand, speak, read or write Welsh?';
local proxyTitle = {
  text: 'Can <em>{person_name}</em> understand, speak, read or write Welsh?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'understand-welsh',
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
