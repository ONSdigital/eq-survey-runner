local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'job-availability-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'job-availability-answer',
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

local nonProxyTitle = 'Are you available to start work in the next two weeks?';
local proxyTitle = {
  text: 'Is <em>{person_name}</em> available to start work in the next two weeks?',
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
