local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, description) = {
  id: 'main-job-type-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'main-job-type-answer',
      mandatory: false,
      options: [
        {
          label: 'Employee',
          value: 'Employee',
        },
        {
          label: 'Self-employed or freelance without employees',
          value: 'Self-employed or freelance without employees',
          description: description,
        },
        {
          label: 'Self-employed with employees',
          value: 'Self-employed with employees',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'In your main job, what is your employment status?';
local proxyTitle = {
  text: 'In their main job, what is <em>{person_name_possessive}</em> employment status?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local pastNonProxyTitle = 'In your main job, what was your employment status?';
local pastProxyTitle = {
  text: 'In their main job, what was <em>{person_name_possessive}</em> employment status?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local nonProxyAnswerDescription = 'Freelance means that you are self-employed and work for different companies or people on particular pieces of work';
local proxyAnswerDescription = 'Freelance means that they are self-employed and work for different companies or people on particular pieces of work';

{
  type: 'Question',
  id: 'main-job-type',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyAnswerDescription),
      when: [rules.isNotProxy, rules.mainJob],
    },
    {
      question: question(proxyTitle, proxyAnswerDescription),
      when: [rules.isProxy, rules.mainJob],
    },
    {
      question: question(pastNonProxyTitle, nonProxyAnswerDescription),
      when: [rules.isNotProxy, rules.lastMainJob],
    },
    {
      question: question(pastProxyTitle, proxyAnswerDescription),
      when: [rules.isProxy, rules.lastMainJob],
    },
  ],
}
