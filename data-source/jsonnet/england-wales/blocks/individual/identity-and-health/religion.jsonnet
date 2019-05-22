local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'What is your religion?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> religion?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local englandDescription = 'Including Church of England, Catholic, Protestant and all other Christian denominations';
local walesDescription = 'All denominations';

local question(title, region_code) = (
  local optionDescription = if region_code == 'GB-WLS' then walesDescription else englandDescription;
  {
    id: 'religion-question',
    title: title,
    description: 'This question is voluntary',
    type: 'General',
    answers: [
      {
        id: 'religion-answer',
        mandatory: false,
        label: 'Select one option only',
        options: [
          {
            label: 'No religion',
            value: 'No religion',
          },
          {
            label: 'Christian',
            value: 'Christian',
            description: optionDescription,
          },
          {
            label: 'Buddhist',
            value: 'Buddhist',
          },
          {
            label: 'Hindu',
            value: 'Hindu',
          },
          {
            label: 'Jewish',
            value: 'Jewish',
          },
          {
            label: 'Muslim',
            value: 'Muslim',
          },
          {
            label: 'Sikh',
            value: 'Sikh',
          },
          {
            label: 'Any other religion',
            value: 'Other',
            detail_answer: {
              id: 'religion-answer-other',
              type: 'TextField',
              mandatory: false,
              label: 'Please specify other religion',
            },
          },
        ],
        type: 'Checkbox',
      },
    ],
  }
);

function(region_code) {
  type: 'Question',
  id: 'religion',
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
