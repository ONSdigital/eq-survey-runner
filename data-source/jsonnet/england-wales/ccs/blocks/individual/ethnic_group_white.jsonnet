local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'Which one best describes your White ethnic group or background?';
local proxyTitle = {
  text: 'Which one best describes {person_name_possessive} White ethnic group or background?',
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
        id: 'white-ethnic-group-answer',
        mandatory: false,
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
            description: 'Select to enter answer',
            detail_answer: {
              id: 'white-ethnic-group-answer-other',
              type: 'TextField',
              mandatory: false,
              label: 'Enter White background',
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
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, region_code),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'another-uk-address',
        when: [rules.under1],
      },
    },
    {
      goto: {
        block: 'past-usual-household-address',
        when: [rules.under4],
      },
    },
    {
      goto: {
        block: 'in-education',
      },
    },
  ],
}
