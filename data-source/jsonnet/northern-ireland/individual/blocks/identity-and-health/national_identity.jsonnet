local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'How would you describe your national identity?';
local proxyTitle = {
  text: 'How would <em>{person_name}</em> describe their national identity?',
  placeholders: [
    placeholders.personName,
  ],
};

local nonProxyDetailAnswerLabel = 'Please describe your national identity';
local proxyDetailAnswerLabel = 'Please describe their national identity';

local question(title, detailAnswerLabel) = {
  id: 'national-identity-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'national-identity-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'British',
          value: 'British',
        },
        {
          label: 'Irish',
          value: 'Irish',
        },
        {
          label: 'Northern Irish',
          value: 'Northern Irish',
        },
        {
          label: 'English',
          value: 'English',
        },
        {
          label: 'Scottish',
          value: 'Scottish',
        },
        {
          label: 'Welsh',
          value: 'Welsh',
        },
        {
          label: 'Other',
          value: 'Other',
          detail_answer: {
            id: 'national-identity-answer-other',
            type: 'TextField',
            mandatory: false,
            label: detailAnswerLabel,
          },
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'national-identity',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDetailAnswerLabel),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, proxyDetailAnswerLabel),
      when: [rules.isProxy],
    },
  ],
}
