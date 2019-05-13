local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'sex-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'sex-answer',
      mandatory: true,
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

local nonProxyTitle = 'What is your sex?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> sex?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};
local guidance = {
  content: [
    {
      title: 'A question about gender will follow',
    },
  ],
};

{
  type: 'Question',
  id: 'sex',
  question_variants: [
    {
      question: question(nonProxyTitle) + {
        guidance: guidance,
      },
      when: [rules.proxyNo, rules.over16],
    },
    {
      question: question(proxyTitle) + {
        guidance: guidance,
      },
      when: [rules.proxyYes, rules.over16],
    },
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
        block: 'marriage-type',
        when: [
          rules.over16,
        ],
      },
    },
    {
      goto: {
        block: 'another-address',
      },
    },
  ],
}
