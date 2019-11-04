local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'other-ethnic-group-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'other-ethnic-group-answer',
      mandatory: false,
      options: [
        {
          label: 'Arab',
          value: 'Arab',
        },
        {
          label: 'Any other ethnic group',
          value: 'Other',
          description: 'Select to enter answer',
          detail_answer: {
            id: 'other-ethnic-group-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Enter other ethnic group',
          },
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Which one best describes your other ethnic group or background?';
local proxyTitle = {
  text: 'Which one best describes {person_name_possessive} other ethnic group or background?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'other-ethnic-group',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'another-uk-address',
        when: [rules.under1],
      },
    },
    {
      goto: {
        block: 'past-usual-household-address',
        when: [rules.under4],
      },
    },
    {
      goto: {
        block: 'in-education',
      },
    },
  ],
}
