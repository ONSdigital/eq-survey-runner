local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'job-availability-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'job-availability-answer',
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

local nonProxyTitle = 'If a job became available now, could you start it within two weeks?';
local proxyTitle = {
  text: 'If a job became available now, could <em>{person_name}</em> start it within two weeks?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'job-availability',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'ever-worked',
        when: [
          {
            id: 'job-availability-answer',
            condition: 'equals',
            value: 'Yes',
          },
        ],
      },
    },
    {
      goto: {
        block: 'job-pending',
      },
    },
  ],
}
