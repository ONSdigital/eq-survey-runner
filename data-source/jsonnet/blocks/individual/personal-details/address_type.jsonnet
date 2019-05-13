local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'address-type-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'address-type-answer',
      mandatory: true,
      options: [
        {
          label: 'Armed forces base address',
          value: 'Armed forces base address',
        },
        {
          label: 'Another address when working away from home',
          value: 'Another address when working away from home',
        },
        {
          label: 'Student’s home address',
          value: 'Student’s home address',
        },
        {
          label: 'Student’s term-time address',
          value: 'Student’s term-time address',
        },
        {
          label: 'Another parent or guardian’s address',
          value: 'Another parent or guardian’s address',
        },
        {
          label: "Partner's address",
          value: "Partner's address",
        },
        {
          label: 'Holiday home',
          value: 'Holiday home',
        },
        {
          label: 'Other',
          value: 'Other',
        },
      ],
      type: 'Checkbox',
    },
  ],
};

local ukAddressTitle = {
  text: 'What type of address is <em>{address}</em>?',
  placeholders: [
    {
      placeholder: 'address',
      transforms: [{
        transform: 'concatenate_list',
        arguments: {
          list_to_concatenate: {
            source: 'answers',
            identifier: ['other-address-answer-building', 'other-address-answer-street'],
          },
          delimiter: ', ',
        },
      }],
    },
  ],
};
local nonProxyNonUkAddressTitle = {
  text: 'What type of address is your address in <em>{country}</em>?',
  placeholders: [
    {
      placeholder: 'country',
      value: {
        source: 'answers',
        identifier: 'another-address-answer-other-country',
      },
    },
  ],
};
local proxyNonUkAddressTitle = {
  text: 'What type of address is <em>{person_name_possessive}</em> address in {country}?',
  placeholders: [
    placeholders.personNamePossessive,
    {
      placeholder: 'country',
      value: {
        source: 'answers',
        identifier: 'another-address-answer-other-country',
      },
    },
  ],
};

{
  type: 'Question',
  id: 'address-type',
  question_variants: [
    {
      question: question(ukAddressTitle),
      when: [
        {
          id: 'another-address-answer',
          condition: 'equals',
          value: 'Yes, an address within the UK',
        },
      ],
    },
    {
      question: question(nonProxyNonUkAddressTitle),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyNonUkAddressTitle),
      when: [rules.proxyYes],
    },
  ],
}
