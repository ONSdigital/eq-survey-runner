local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, guidanceHeader) = {
  id: 'jobseeker-question',
  title: title,
  type: 'General',
  answers: [
    {
      guidance: {
        show_guidance: guidanceHeader,
        hide_guidance: guidanceHeader,
        contents: [
          {
            description: 'To get a true picture of the UK working population, we ask this question of everyone who is not currently working. We ask people who are retired because the number of people continuing to work after retirement age is increasing. We ask people who are long-term sick or disabled because some intend to go back to work.',
          },
        ],
      },
      id: 'jobseeker-answer',
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

local nonProxyTitle = 'In the last four weeks, were you actively looking for any kind of paid work?';
local proxyTitle = {
  text: 'In the last four weeks, was <em>{person_name}</em> actively looking for any kind of paid work?',
  placeholders: [
    placeholders.personName,
  ],
};
local nonProxyGuidanceHeader = 'Why do I need to answer if I am retired or long-term sick or disabled?';
local proxyGuidanceHeader = 'Why do I need to answer if they have retired or are long-term sick or disabled?';

{
  type: 'Question',
  id: 'jobseeker',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyGuidanceHeader),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, proxyGuidanceHeader),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'job-pending',
        when: [
          {
            id: 'jobseeker-answer',
            condition: 'equals',
            value: 'No',
          },
        ],
      },
    },
    {
      goto: {
        block: 'job-availability',
      },
    },
  ],
}
