local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'sexual-identity-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'sexual-identity-answer',
      mandatory: false,
      label: '',
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
            label: 'Please specify sexual orientation',
          },
        },
        {
          label: 'Prefer not to say',
          value: 'Prefer not to say',
        },
      ],
      type: 'Checkbox',
    },
  ],
};

local nonProxyTitle = 'Which of the following best describes your sexual orientation?';

local proxyTitle = {
  text: 'Which of the following best describes <em>{person_name_possessive}</em> sexual orientation?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'sexual-identity',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle),
      when: [rules.proxyYes],
    },
  ],
}
