local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'job-title-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'job-title-answer',
      label: 'Job title',
      mandatory: true,
      type: 'TextField',
    },
  ],
};

local nonProxyTitle = 'What is your full job title?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> full job title?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local pastNonProxyTitle = 'What was your full job title?';
local pastProxyTitle = {
  text: 'What was <em>{person_name_possessive}</em> full job title?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'job-title',
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
}
