local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'sex-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'sex-answer',
      mandatory: false,
      options: [
        {
          label: 'Female',
          value: 'Female',
        },
        {
          label: 'Male',
          value: 'Male',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Can I confirm your sex?';
local proxyTitle = {
  text: 'What is {person_name_possessive} sex?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'sex',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy, rules.over16],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy, rules.over16],
    },
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy, rules.estimatedAge],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy, rules.estimatedAge],
    },
  ],
}
