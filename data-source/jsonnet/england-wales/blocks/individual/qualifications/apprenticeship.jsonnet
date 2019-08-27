local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'Have you completed an apprenticeship?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> completed an apprenticeship?',
  placeholders: [
    placeholders.personName,
  ],
};

local walesGuidanceTitle = 'Include equivalent apprenticeships completed anywhere outside Wales and England';
local englandGuidanceTitle = 'Include equivalent apprenticeships completed anywhere outside England and Wales';
local walesAnswerDescription = 'For example, trade, higher, foundation or modern';
local englandAnswerDescription = 'For example, trade, advanced, foundation or modern';

local question(title, region_code) = (
  local regionGuidanceTitle = if region_code == 'GB-WLS' then walesGuidanceTitle else englandGuidanceTitle;
  local answerDescription = if region_code == 'GB-WLS' then walesAnswerDescription else englandAnswerDescription;
  {
    id: 'apprenticeship-question',
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
        id: 'apprenticeship-answer',
        mandatory: false,
        options: [
          {
            label: 'Yes',
            value: 'Yes',
            description: answerDescription,
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
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, region_code),
      when: [rules.isProxy],
    },
  ],
}
