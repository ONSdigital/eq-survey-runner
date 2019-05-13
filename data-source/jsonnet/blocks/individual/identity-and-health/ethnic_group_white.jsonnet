local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local nonProxyTitle = 'Which one best describes your White ethnic group or background?';
local proxyTitle = {
  text: 'Which one best describes <em>{person_name_possessive}</em> White ethnic group or background?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local englandOption = 'English, Welsh, Scottish, Northern Irish or British';
local walesOption = 'Welsh, English, Scottish, Northern Irish or British';

local question(title, region_code) = (
  local radioOptions = if region_code == 'GB-WLS' then walesOption else englandOption;
  {
    id: 'white-ethnic-group-question',
    title: title,
    type: 'General',
    answers: [
      {
        guidance: {
          show_guidance: 'Why your answer is important',
          hide_guidance: 'Why your answer is important',
          content: [
            {
              description: 'How you define your ethnic group is up to you. Sharing this information enables the government and other organisations to provide appropriate resources and policies such as housing, education, health and criminal justice.',
            },
          ],
        },
        id: 'white-ethnic-group-answer',
        mandatory: true,
        options: [
          {
            label: radioOptions,
            value: radioOptions,
          },
          {
            label: 'Irish',
            value: 'Irish',
          },
          {
            label: 'Gypsy or Irish Traveller',
            value: 'Gypsy or Irish Traveller',
          },
          {
            label: 'Roma',
            value: 'Roma',
          },
          {
            label: 'Any other White background',
            value: 'Other',
            detail_answer: {
              id: 'white-ethnic-group-answer-other',
              type: 'TextField',
              mandatory: false,
              label: 'Please specify White background',
            },
          },
        ],
        type: 'Radio',
      },
    ],
  }
);

function(region_code) {
  type: 'Question',
  id: 'white-ethnic-group',
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
        block: 'religion',
      },
    },
  ],
}
