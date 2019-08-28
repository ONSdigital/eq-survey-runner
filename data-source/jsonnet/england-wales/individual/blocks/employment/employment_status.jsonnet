local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, description) = {
  id: 'employment-status-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: true,
  guidance: {
    contents: [
      {
        description: 'Include casual or temporary work, even if only for one hour',
      },
    ],
  },
  answers: [
    {
      id: 'employment-status-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'Working as an employee',
          value: 'Working as an employee',
        },
        {
          label: 'Self-employed or freelance',
          value: 'Self-employed or freelance',
          description: description,
        },
        {
          label: 'Temporarily away from work ill, on holiday or temporarily laid off',
          value: 'Temporarily away from work ill, on holiday or temporarily laid off',
        },
        {
          label: 'On maternity or paternity leave',
          value: 'On maternity or paternity leave',
        },
        {
          label: 'Doing any other kind of paid work',
          value: 'Doing any other kind of paid work',
        },
      ],
    },
    {
      id: 'employment-status-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'None of these apply',
          value: 'None of these apply',
        },
      ],
    },
  ],
};

local nonProxyTitle = 'In the last seven days, were you doing any of the following?';
local proxyTitle = {
  text: 'In the last seven days, was <em>{person_name}</em> doing any of the following?',
  placeholders: [
    placeholders.personName,
  ],
};

local nonProxyAnswerDescription = 'Freelance means that you are self-employed and work for different companies or people on particular pieces of work';
local proxyAnswerDescription = 'Freelance means that they are self-employed and work for different companies or people on particular pieces of work';

{
  type: 'Question',
  id: 'employment-status',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyAnswerDescription),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, proxyAnswerDescription),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'employment-type',
        when: [
          rules.lastMainJob,
        ],
      },
    },
    {
      goto: {
        block: 'main-employment-block',
      },
    },
  ],
}
