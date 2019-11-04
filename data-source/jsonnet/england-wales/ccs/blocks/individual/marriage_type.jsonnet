local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'marriage-type-question',
  title: title,
  instruction: 'Tell respondent to turn to <strong>Showcard 8</strong>',
  type: 'General',
  answers: [
    {
      id: 'marriage-type-answer',
      mandatory: false,
      options: [
        {
          label: 'Never married and never registered a civil partnership',
          value: 'Never',
        },
        {
          label: 'Married',
          value: 'Married',
        },
        {
          label: 'In a registered civil partnership',
          value: 'In a registered civil partnership',
        },
        {
          label: 'Separated, but still legally married',
          value: 'Separated, but still legally married',
        },
        {
          label: 'Separated, but still legally in a civil partnership',
          value: 'Separated, but still legally in a civil partnership',
        },
        {
          label: 'Divorced',
          value: 'Divorced',
        },
        {
          label: 'Formerly in a civil partnership which is now legally dissolved',
          value: 'Formerly in a civil partnership which is now legally dissolved',
        },
        {
          label: 'Widowed',
          value: 'Widowed',
        },
        {
          label: 'Surviving partner from a registered civil partnership',
          value: 'Surviving partner from a registered civil partnership',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle(census_date) = {
  text: 'On {census_date}, what was your legal marital or registered civil partnership status?',
  placeholders: [
    placeholders.censusDate(census_date),
  ],
};
local proxyTitle(census_date) = {
  text: 'On {census_date}, what was {person_name_possessive} legal marital or registered civil partnership status?',
  placeholders: [
    placeholders.censusDate(census_date),
    placeholders.personNamePossessive,
  ],
};

function(census_date) {
  type: 'Question',
  id: 'marriage-type',
  question_variants: [
    {
      question: question(nonProxyTitle(census_date)),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle(census_date)),
      when: [rules.isProxy],
    },
  ],
}
