local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'confirm-date-of-birth',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'confirm-date-of-birth-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No',
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

local proxyTitle = {
  text: '{person_name} is {age_in_years} years old. Is this correct?',
  placeholders: [
    placeholders.personName,
    dateOfBirthPlaceholder,
  ],
};

{
  type: 'ConfirmationQuestion',
  id: 'confirm-dob',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
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
