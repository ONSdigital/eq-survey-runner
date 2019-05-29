local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title, guidance) = {
  id: 'school-travel-mode-question',
  title: title,
  guidance: {
    content: [
      {
        title: guidance,
      },
    ],
  },
  type: 'General',
  answers: [
    {
      id: 'school-travel-mode-answer',
      mandatory: true,
      options: [
        {
          label: 'Driving a car or van',
          value: 'Driving a car or van',
        },
        {
          label: 'Passenger in a car or van',
          value: 'Passenger in a car or van',
        },
        {
          label: 'Car or van pool, sharing driving',
          value: 'Car or van pool, sharing driving',
        },
        {
          label: 'Bus, minibus or coach (public or private)',
          value: 'Bus, minibus or coach (public or private)',
        },
        {
          label: 'On foot',
          value: 'On foot',
        },
        {
          label: 'Taxi',
          value: 'Taxi',
        },
        {
          label: 'Train',
          value: 'Train',
        },
        {
          label: 'Bicycle',
          value: 'Bicycle',
        },
        {
          label: 'Motorcycle, scooter or moped',
          value: 'Motorcycle, scooter or moped',
        },
        {
          label: 'Other',
          value: 'Other',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'How do you usually travel to your place of study, including school?';
local nonProxyGuidance = 'Select one option only, for the longest part, by distance, of your usual journey to place of study.';
local proxyTitle = {
  text: 'How does <em>{person_name}</em> usually travel to their place of study, including school?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyGuidance = 'Select one option only, for the longest part, by distance, of their usual journey to place of study.';

{
  type: 'Question',
  id: 'school-travel-mode',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyGuidance),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyGuidance),
      when: [rules.proxyYes],
    },
  ],
}
