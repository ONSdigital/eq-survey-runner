local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'What religion, religious denomination or body were you <em>brought up</em> in?';
local proxyTitle = {
  text: 'What religion, religious denomination or body was {person_name} <em>brought up</em> in?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'no-religion-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'no-religion-answer',
      mandatory: false,
      label: 'Select one option only',
      options: [
        {
          label: 'Roman Catholic',
          value: 'Roman Catholic',
        },
        {
          label: 'Presbyterian Church in Ireland',
          value: 'Presbyterian Church in Ireland',
        },
        {
          label: 'Church of Ireland',
          value: 'Church of Ireland',
        },
        {
          label: 'Methodist Church in Ireland',
          value: 'Methodist Church in Ireland',
        },
        {
          label: 'Other',
          value: 'Other',
          detail_answer: {
            id: 'no-religion-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify religion, religious denomination or body',
          },
        },
        {
          label: 'None',
          value: 'None',
        },
      ],
      type: 'Radio',
    },
  ],
};

{
  type: 'Question',
  id: 'no-religion',
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
