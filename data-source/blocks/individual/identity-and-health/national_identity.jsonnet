local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, options) = {
  id: 'national-identity-question',
  title: title,
  type: 'General',
  definitions: [
    {
      title: "What do we mean by 'national identity'?",
      content: [
        {
          description: 'National Identity is not dependent on your ethnic group or citizenship. This could be about the country or countries where you feel you belong, or think of as home.',
        },
      ],
    },
  ],
  answers: [
    {
      id: 'national-identity-answer',
      mandatory: true,
      type: 'Checkbox',
    } + options,
  ],
};

local nonProxyTitle = 'How would you describe your national identity?';
local proxyTitle = {
  text: 'How would <em>{person_name}</em> describe their national identity?',
  placeholders: [
    placeholders.personName,
  ],
};

local englandOptions = {
  options: [
    {
      label: 'English',
      value: 'English',
    },
    {
      label: 'Welsh',
      value: 'Welsh',
    },
    {
      label: 'Scottish',
      value: 'Scottish',
    },
    {
      label: 'Northern Irish',
      value: 'Northern Irish',
    },
    {
      label: 'British',
      value: 'British',
    },
    {
      label: 'Other',
      value: 'Other',
      detail_answer: {
        id: 'national-identity-england-answer-other',
        type: 'TextField',
        mandatory: false,
        label: 'Please describe your national identity',
      },
    },
  ],
};

local walesOptions = {
  options: [
    {
      label: 'Welsh',
      value: 'Welsh',
    },
    {
      label: 'English',
      value: 'English',
    },
    {
      label: 'Scottish',
      value: 'Scottish',
    },
    {
      label: 'Northern Irish',
      value: 'Northern Irish',
    },
    {
      label: 'British',
      value: 'British',
    },
    {
      label: 'Other',
      value: 'Other',
      detail_answer: {
        id: 'national-identity-wales-answer-other',
        type: 'TextField',
        mandatory: false,
        label: 'Please describe your national identity',
      },
    },
  ],
};

{
  type: 'Question',
  id: 'national-identity',
  question_variants: [
    {
      question: question(nonProxyTitle, englandOptions),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, englandOptions),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, walesOptions),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, walesOptions),
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
}
