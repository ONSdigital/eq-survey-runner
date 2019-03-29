local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, label) = {
  id: 'sexual-identity-question',
  title: title,
  type: 'General',
  description: 'This question is voluntary',
  answers: [
    {
      id: 'sexual-identity-answer',
      mandatory: true,
      label: 'Select one option only',
      options: [
        {
          label: 'Straight or Heterosexual',
          value: 'Straight or Heterosexual',
        },
        {
          label: 'Gay or Lesbian',
          value: 'Gay or Lesbian',
        },
        {
          label: 'Bisexual',
          value: 'Bisexual',
        },
        {
          label: 'Other sexual orientation',
          value: 'Other sexual orientation',
          detail_answer: {
            id: 'sexual-identity-answer-other',
            type: 'TextField',
            mandatory: false,
            label: label,
          },
        },
      ],
      type: 'Checkbox',
    },
  ],
};

local nonProxyTitle = 'Which of the following best describes your sexual orientation?';
local nonProxyLabel = 'Please specify your sexual orientation';
local proxyTitle = {
  text: 'Which of the following best describes <em>{person_name_possessive}</em> sexual orientation?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};
local proxyLabel = 'Please specify their sexual orientation';

{
  type: 'Question',
  id: 'sexual-identity',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyLabel),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyLabel),
      when: [rules.proxyYes],
    },
  ],
}
