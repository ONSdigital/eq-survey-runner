local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'jobseeker-question',
  title: title,
  type: 'General',
  answers: [
    {
      guidance: {
        show_guidance: 'Why do I need to answer if I am retired or long term sick or disabled?',
        hide_guidance: 'Why do I need to answer if I am retired or long term sick or disabled',
        content: [
          {
            description: 'To get a true picture of the UK working population, we ask this question to everyone who is not currently working. We ask people who are retired because the number of people continuing to work after retirement age is increasing. We ask people who are long-term sick or disabled because some intend to go back to work.',
          },
        ],
      },
      id: 'jobseeker-answer',
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

local nonProxyTitle = 'In the last four weeks, were you actively looking for any kind of paid work?';
local proxyTitle = {
  text: 'In the last four weeks, was <em>{person_name}</em> actively looking for any kind of paid work?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'jobseeker',
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
        block: 'job-availability',
        when: [
          {
            id: 'jobseeker-answer',
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
