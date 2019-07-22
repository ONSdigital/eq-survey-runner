local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, yesLabel, noLabel) = {
  id: 'confirm-date-of-birth',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'confirm-date-of-birth-answer',
      mandatory: true,
      options: [
        {
          label: yesLabel,
          value: 'Yes',
        },
        {
          label: noLabel,
          value: 'No',
        },
      ],
      type: 'Radio',
    },
  ],
};

local dateOfBirthPlaceholder = {
  placeholder: 'age_in_years',
  transforms: [
    {
      transform: 'calculate_years_difference',
      arguments: {
        first_date: {
          source: 'answers',
          identifier: 'date-of-birth-answer',
        },
        second_date: {
          value: 'now',
        },
      },
    },
  ],
};

local nonProxyTitle = {
  text: 'You are {age_in_years} years old. Is this correct?',
  placeholders: [
    dateOfBirthPlaceholder,
  ],
};
local nonProxyYesLabel = {
  text: 'Yes, I am {age_in_years} years old',
  placeholders: [
    dateOfBirthPlaceholder,
  ],
};
local nonProxyNoLabel = 'No, I need to change my date of birth';

local proxyTitle = {
  text: '{person_name} is {age_in_years} years old. Is this correct?',
  placeholders: [
    placeholders.personName,
    dateOfBirthPlaceholder,
  ],
};
local proxyYesLabel = {
  text: 'Yes, {person_name} is {age_in_years} years old',
  placeholders: [
    placeholders.personName,
    dateOfBirthPlaceholder,
  ],
};
local proxyNoLabel = 'No, I need to change their date of birth';

{
  type: 'ConfirmationQuestion',
  id: 'confirm-dob',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyYesLabel, nonProxyNoLabel),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyYesLabel, proxyNoLabel),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'date-of-birth',
        when: [
          {
            id: 'confirm-date-of-birth-answer',
            condition: 'equals',
            value: 'No',
          },
        ],
      },
    },
    {
      goto: {
        block: 'sex',
      },
    },
  ],
}
