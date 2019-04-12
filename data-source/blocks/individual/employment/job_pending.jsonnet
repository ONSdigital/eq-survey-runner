local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'job-pending-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'job-pending-answer',
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

local nonProxyTitle = 'In the last seven days, were you waiting to start a job already accepted?';
local proxyTitle = {
  text: 'In the last seven days, was <em>{person_name}</em> waiting to start a job already accepted?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'job-pending',
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
