local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'Have you achieved any other qualifications, either within or outside of Northern Ireland?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved any other qualifications?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'other-qualifications-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: true,
  answers: [
    {
      id: 'other-qualifications-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'Yes, in England or Wales',
          value: 'Yes, in England or Wales',
        },
        {
          label: 'Yes, anywhere outside of England and Wales',
          value: 'Yes, anywhere outside of England and Wales',
        },
      ],
    },
    {
      id: 'other-qualifications-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'No qualifications',
          value: 'No qualifications',
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'other-qualifications',
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
