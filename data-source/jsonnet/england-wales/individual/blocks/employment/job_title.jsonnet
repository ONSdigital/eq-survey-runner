local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, description) = {
  id: 'job-title-question',
  title: title,
  type: 'General',
  description: description,
  answers: [
    {
      id: 'job-title-answer',
      label: 'Job title',
      mandatory: false,
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

local nonProxyDescription = 'For example, retail assistant, office cleaner, district nurse, primary school teacher. Do not state your grade or pay band';
local proxyDescription = 'For example, retail assistant, office cleaner, district nurse, primary school teacher. Do not state their grade or pay band';

{
  type: 'Question',
  id: 'job-title',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDescription),
      when: [rules.isNotProxy, rules.mainJob],
    },
    {
      question: question(proxyTitle, proxyDescription),
      when: [rules.isProxy, rules.mainJob],
    },
    {
      question: question(pastNonProxyTitle, nonProxyDescription),
      when: [rules.isNotProxy, rules.lastMainJob],
    },
    {
      question: question(pastProxyTitle, proxyDescription),
      when: [rules.isProxy, rules.lastMainJob],
    },
  ],
}
