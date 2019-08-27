local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

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

local englandDescription = 'For example, clothing retail, general hospital, primary education, food wholesale, civil service DWP, local government housing.';
local walesDescription = 'For example, clothing retail, general hospital, primary education, food wholesale, civil service (Welsh Government), local government (housing).';

local question(title, region_code) = (
  local description = if region_code == 'GB-WLS' then walesDescription else englandDescription;
  {
    id: 'employers-business-question',
    title: title,
    description: description,
    type: 'General',
    answers: [
      {
        id: 'employers-business-answer',
        label: 'Main activity',
        mandatory: false,
        type: 'TextField',
      },
    ],
  }
);

function(region_code) {
  type: 'Question',
  id: 'employers-business',
  question_variants: [
    {
      question: question(nonProxyTitle, region_code),
      when: [rules.isNotProxy, rules.mainJob],
    },
    {
      question: question(proxyTitle, region_code),
      when: [rules.isProxy, rules.mainJob],
    },
    {
      question: question(pastNonProxyTitle, region_code),
      when: [rules.isNotProxy, rules.lastMainJob],
    },
    {
      question: question(pastProxyTitle, region_code),
      when: [rules.isProxy, rules.lastMainJob],
    },
  ],
}
