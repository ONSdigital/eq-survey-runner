local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'supervise-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'supervise-answer',
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

local nonProxyTitle = 'Do you supervise or oversee the work of other employees on a day-to-day basis?';
local proxyTitle = {
  text: 'Does <em>{person_name}</em> supervise or oversee the work of other employees on a day-to-day basis?',
  placeholders: [
    placeholders.personName,
  ],
};

local pastNonProxyTitle = 'Did you supervise or oversee the work of other employees on a day-to-day basis?';
local pastProxyTitle = {
  text: 'Did <em>{person_name}</em> supervise or oversee the work of other employees on a day-to-day basis?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'supervise',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.proxyNo, rules.mainJob],
    },
    {
      question: question(proxyTitle),
      when: [rules.proxyYes, rules.mainJob],
    },
    {
      question: question(pastNonProxyTitle),
      when: [rules.proxyNo, rules.lastMainJob],
    },
    {
      question: question(pastProxyTitle),
      when: [rules.proxyYes, rules.lastMainJob],
    },
  ],
  routing_rules: [
    {
      goto: {
        group: 'comments-group',
        when: [
          rules.lastMainJob,
        ],
      },
    },
    {
      goto: {
        block: 'hours-worked',
      },
    },
  ],
}
