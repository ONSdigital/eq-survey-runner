local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'Have you achieved an NVQ or equivalent qualification?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved an NVQ or equivalent qualification?',
  placeholders: [
    placeholders.personName,
  ],
};

local englandGuidanceTitle = 'Include equivalent qualifications achieved anywhere outside England and Wales';
local walesGuidanceTitle = 'Include equivalent qualifications achieved anywhere outside Wales and England';

local question(title, region_code) = (
  local regionGuidanceTitle = if region_code == 'GB-WLS' then walesGuidanceTitle else englandGuidanceTitle;
  {
    id: 'nvq-level-question',
    title: title,
    type: 'MutuallyExclusive',
    guidance: {
      contents: [
        {
          description: regionGuidanceTitle,
        },
      ],
    },
    mandatory: false,
    answers: [
      {
        id: 'nvq-level-answer',
        mandatory: false,
        type: 'Checkbox',
        options: [
          {
            label: 'NVQ level 3 or equivalent',
            value: 'NVQ level 3 or equivalent',
            description: 'For example, BTEC National, OND or ONC, City and Guilds Advanced Craft',
          },
          {
            label: 'NVQ level 2 or equivalent',
            value: 'NVQ level 2 or equivalent',
            description: 'For example, BTEC General, City and Guilds Craft',
          },
          {
            label: 'NVQ level 1 or equivalent',
            value: 'NVQ level 1 or equivalent',
          },
        ],
      },
      {
        id: 'nvq-level-answer-exclusive',
        type: 'Checkbox',
        mandatory: false,
        options: [
          {
            label: 'None of these apply',
            value: 'None of these apply',
            description: 'Questions on A levels, GCSEs and equivalents will follow',
          },
        ],
      },
    ],
  }
);

function(region_code) {
  type: 'Question',
  id: 'nvq-level',
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
