local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'Have you achieved any other qualifications?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved any other qualifications?',
  placeholders: [
    placeholders.personName,
  ],
};

local englandOptions = [
  {
    label: 'Yes, in England or Wales',
    value: 'Yes, in England or Wales',
  },
  {
    label: 'Yes, anywhere outside of England and Wales',
    value: 'Yes, anywhere outside of England and Wales',
  },
];

local walesOptions = [
  {
    label: 'Yes, in Wales or England',
    value: 'Yes, in Wales or England',
  },
  {
    label: 'Yes, anywhere outside of Wales and England',
    value: 'Yes, anywhere outside of Wales and England',
  },
];

local question(title, region_code) = (
  local regionOptions = if region_code == 'GB-WLS' then walesOptions else englandOptions;
  {
    id: 'other-qualifications-question',
    title: title,
    type: 'MutuallyExclusive',
    mandatory: true,
    answers: [
      {
        id: 'other-qualifications-answer',
        mandatory: false,
        type: 'Checkbox',
        options: regionOptions,
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
  }
);

function(region_code) {
  type: 'Question',
  id: 'other-qualifications',
  question_variants: [
    {
      question: question(nonProxyTitle, region_code),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, region_code),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        group: 'employment-group',
      },
    },
  ],
}
