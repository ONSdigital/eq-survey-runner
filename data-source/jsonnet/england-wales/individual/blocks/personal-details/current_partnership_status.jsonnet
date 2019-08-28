local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'currrent-partnership-status-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'current-partnership-status-answer',
      mandatory: false,
      options: [
        {
          label: 'Someone of the opposite sex',
          value: 'Someone of the opposite sex',
        },
        {
          label: 'Someone of the same sex',
          value: 'Someone of the same sex',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Who is your registered civil partnership to?';
local proxyTitle = {
  text: 'Who is <em>{person_name_possessive}</em> registered civil partnership to?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'current-partnership-status',
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
        block: 'another-address',
      },
    },
  ],
}
