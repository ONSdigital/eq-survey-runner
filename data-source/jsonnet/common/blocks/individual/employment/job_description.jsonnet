local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'job-description-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'job-description-answer',
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

local nonProxyTitle = 'Briefly describe what you do in your main job?';
local proxyTitle = {
  text: 'Briefly describe what <em>{person_name}</em> does in their main job?',
  placeholders: [
    placeholders.personName,
  ],
};

local pastNonProxyTitle = 'Briefly describe what you did in your main job?';
local pastProxyTitle = {
  text: 'Briefly describe what <em>{person_name}</em> did in their main job?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'job-description',
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
