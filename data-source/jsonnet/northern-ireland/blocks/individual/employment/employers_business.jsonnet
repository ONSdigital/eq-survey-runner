local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

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

local question(title) = (
  {
    id: 'employers-business-question',
    title: title,
    description: 'For example clothing retail, general hospital, primary education, food wholesale, civil service, local government housing.',
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
  }
);

{
  type: 'Question',
  id: 'employers-business',
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
