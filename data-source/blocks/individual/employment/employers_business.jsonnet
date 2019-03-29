local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description) = {
  id: 'employers-business-question',
  title: title,
  description: description,
  type: 'General',
  answers: [
    {
      id: 'employers-business-answer',
      label: 'Description',
      mandatory: true,
      type: 'TextArea',
      max_length: 200,
      validation: {
        messages: {
          MAX_LENGTH_EXCEEDED: 'Your answer has to be less than %(max)d characters long',
        },
      },
    },
  ],
};

local nonProxyTitle = 'What is the main activity of your organisation, business or freelance work?';
local proxyTitle = {
  text: 'What is the main activity of <em>{person_name_possessive}</em> organisation, business or freelance work?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local pastNonProxyTitle = 'What was the main activity of your organisation, business or freelance work?';
local pastProxyTitle = {
  text: 'What was the main activity of <em>{person_name_possessive}</em> organisation, business or freelance work?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local englandDescription = 'For example clothing retail, general hospital, primary education, food wholesale, civil service DWP, local government housing.';
local walesDescription = 'For example clothing retail, general hospital, primary education, food wholesale, civil service DVLA, local government housing.';

{
  type: 'Question',
  id: 'employers-business',
  question_variants: [
    {
      question: question(nonProxyTitle, englandDescription),
      when: [rules.proxyNo, rules.mainJob, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, englandDescription),
      when: [rules.proxyYes, rules.mainJob, rules.regionNotWales],
    },
    {
      question: question(pastNonProxyTitle, englandDescription),
      when: [rules.proxyNo, rules.lastMainJob, rules.regionNotWales],
    },
    {
      question: question(pastProxyTitle, englandDescription),
      when: [rules.proxyYes, rules.lastMainJob, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, walesDescription),
      when: [rules.proxyNo, rules.mainJob, rules.regionWales],
    },
    {
      question: question(proxyTitle, walesDescription),
      when: [rules.proxyYes, rules.mainJob, rules.regionWales],
    },
    {
      question: question(pastNonProxyTitle, walesDescription),
      when: [rules.proxyNo, rules.lastMainJob, rules.regionWales],
    },
    {
      question: question(pastProxyTitle, walesDescription),
      when: [rules.proxyYes, rules.lastMainJob, rules.regionWales],
    },
  ],
}
