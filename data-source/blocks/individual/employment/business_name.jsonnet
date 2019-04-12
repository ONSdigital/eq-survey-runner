local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description, option) = {
  id: 'business-name-question',
  title: title,
  description: description,
  type: 'MutuallyExclusive',
  mandatory: true,
  answers: [
    {
      id: 'business-name-answer',
      label: 'Organisation or business name',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'no-business-name-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: option,
          value: option,
        },
      ],
    },
  ],
};

local nonProxyTitle = 'What is the name of the organisation or business you work for?';
local nonProxyDescription = 'If you are self-employed in your own business, give the business name.';
local proxyTitle = {
  text: 'What is the name of the organisation or business <em>{person_name}</em> works for?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyDescription = 'If they are self-employed in their own business, give the business name.';
local option = 'No organisation or work for a private individual';

local pastNonProxyTitle = 'What was the name of the organisation or business you worked for?';
local pastNonProxyDescription = 'If you were self-employed in your own business, give the business name.';
local pastNonProxyOption = '';
local pastProxyTitle = {
  text: 'What was the name of the organisation or business <em>{person_name}</em> worked for?',
  placeholders: [
    placeholders.personName,
  ],
};
local pastProxyDescription = 'If they were self-employed in their own business, give the business name.';
local pastOption = 'No organisation or worked for a private individual';

{
  type: 'Question',
  id: 'business-name',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDescription, option),
      when: [rules.proxyNo, rules.mainJob],
    },
    {
      question: question(proxyTitle, proxyDescription, option),
      when: [rules.proxyYes, rules.mainJob],
    },
    {
      question: question(pastNonProxyTitle, pastNonProxyDescription, pastOption),
      when: [rules.proxyNo, rules.lastMainJob],
    },
    {
      question: question(pastProxyTitle, pastProxyDescription, pastOption),
      when: [rules.proxyYes, rules.lastMainJob],
    },
  ],
}
