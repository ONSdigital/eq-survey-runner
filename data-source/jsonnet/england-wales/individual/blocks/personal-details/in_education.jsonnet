local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'in-education-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'in-education-answer',
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


local nonProxyUnder19Title = 'Are you a schoolchild or student in full-time education?';
local proxyUnder19Title = {
  text: 'Is <em>{person_name}</em> a schoolchild or student in full-time education?',
  placeholders: [
    placeholders.personName,
  ],
};
local nonProxyOver19Title = 'Are you a student in full-time education?';
local proxyOver19Title = {
  text: 'Is <em>{person_name}</em> a student in full-time education?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'in-education',
  question_variants: [
    {
      question: question(nonProxyOver19Title),
      when: [rules.isNotProxy, rules.over19],
    },
    {
      question: question(proxyOver19Title),
      when: [rules.isProxy, rules.over19],
    },
    {
      question: question(nonProxyUnder19Title),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyUnder19Title),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'term-time-location',
        when: [
          {
            id: 'in-education-answer',
            condition: 'equals',
            value: 'Yes',
          },
        ],
      },
    },
    {
      goto: {
        group: 'identity-and-health-group',
      },
    },
  ],
}
