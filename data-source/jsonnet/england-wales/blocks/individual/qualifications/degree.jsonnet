local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'Have you achieved a qualification at degree level or above?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved a qualification at degree level or above?',
  placeholders: [
    placeholders.personName,
  ],
};

local englandGuidanceTitle = 'Include equivalent qualifications achieved anywhere outside England and Wales';
local walesGuidanceTitle = 'Include equivalent qualifications achieved anywhere outside Wales and England';

local question(title, region_code) = (
  local regionGuidanceTitle = if region_code == 'GB-WLS' then walesGuidanceTitle else englandGuidanceTitle;
  {
    id: 'degree-question',
    title: title,
    type: 'General',
    guidance: {
      contents: [
        {
          description: regionGuidanceTitle,
        },
      ],
    },
    answers: [
      {
        id: 'degree-answer',
        mandatory: false,
        type: 'Radio',
        options: [
          {
            label: 'Yes',
            value: 'Yes',
            description: 'For example, degree, foundation degree, HND or HNC, NVQ level 4 and above, teaching or nursing',
          },
          {
            label: 'No',
            value: 'No',
            description: 'Questions on other NVQs, A levels, GCSEs and equivalents will follow',
          },
        ],
      },
    ],
  }
);

function(region_code) {
  type: 'Question',
  id: 'degree',
  question_variants: [
    {
      question: question(nonProxyTitle, region_code),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, region_code),
      when: [rules.isProxy],
    },
  ],
}
