local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'sexual-identity-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: false,
  answers: [
    {
      id: 'sexual-identity-answer',
      mandatory: false,
      type: 'Checkbox',
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
      ],
    },
    {
      id: 'sexual-identity-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'Prefer not to say',
          value: 'Prefer not to say',
        },
      ],
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
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
  ],
}
