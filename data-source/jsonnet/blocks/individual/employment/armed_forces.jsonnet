local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'armed-forces-question',
  title: title,
  guidance: {
    content: [
      {
        title: 'Current serving members should select “No”',
      },
    ],
  },
  type: 'General',
  answers: [
    {
      id: 'armed-forces-answer',
      mandatory: true,
      guidance: {
        show_guidance: 'Why your answer is important',
        hide_guidance: 'Why your answer is important',
        content: [
          {
            description: 'We are measuring the number of people who have served in the UK Armed Forces and have now left. Government and councils need this information to carry out their commitments made under the Armed Forces Covenant. This is a promise by the nation ensuring that those who serve or who have served in the armed forces, and their families, are not disadvantaged.',
          },
        ],
      },
      options: [
        {
          label: 'No',
          value: 'No',
        },
        {
          label: 'Yes, previously served in Regular Armed Forces',
          value: 'Yes, previously served in Regular Armed Forces',
        },
        {
          label: 'Yes, previously served in Reserve Armed Forces',
          value: 'Yes, previously served in Reserve Armed Forces',
        },
      ],
      type: 'Checkbox',
    },
  ],
};

local nonProxyTitle = 'Have you previously served in the UK Armed Forces?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> previously served in the UK Armed Forces?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'armed-forces',
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
