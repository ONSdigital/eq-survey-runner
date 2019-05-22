local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'Have you completed an apprenticeship?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> completed an apprenticeship?',
  placeholders: [
    placeholders.personName,
  ],
};

local walesGuidanceTitle = 'Include equivalent apprenticeships completed anywhere outside Wales and England';
local englandGuidanceTitle = 'Include equivalent apprenticeships completed anywhere outside England and Wales';

local question(title, region_code) = (
  local regionGuidanceTitle = if region_code == 'GB-WLS' then walesGuidanceTitle else englandGuidanceTitle;
  {
    id: 'apprenticeship-question',
    title: title,
    type: 'General',
    guidance: {
      content: [
        {
          title: regionGuidanceTitle,
        },
      ],
    },
    answers: [
      {
        id: 'apprenticeship-answer',
        mandatory: true,
        options: [
          {
            label: 'Yes',
            value: 'Yes',
            description: 'For example trade, advanced, foundation, modern',
          },
          {
            label: 'No',
            value: 'No',
          },
        ],
        type: 'Radio',
      },
    ],
  }
);

function(region_code) {
  type: 'Question',
  id: 'apprenticeship',
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
}
