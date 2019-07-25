local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description) = {
  title: title,
  id: 'work-travel-question',
  description: description,
  type: 'General',
  answers: [
    {
      id: 'work-travel-answer',
      mandatory: false,
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

local nonProxyTitleWork = 'How do you usually travel to your main place of work?';
local proxyTitleWork = {
  text: 'How does <em>{person_name}</em> usually travel to their main place of work?',
  placeholders: [
    placeholders.personName,
  ],
};

local pastNonProxyTitleWork = 'How did you usually travel to your main place of work?';
local pastProxyTitleWork = {
  text: 'How did <em>{person_name}</em> usually travel to their main place of work?',
  placeholders: [
    placeholders.personName,
  ],
};

local nonProxyDescriptionWork = 'Select one option only, for the longest part, by distance, of your usual journey to place of work.';
local proxyDescriptionWork = 'Select one option only, for the longest part, by distance, of their usual journey to place of work.';

{
  type: 'Question',
  id: 'work-travel',
  question_variants: [
    {
      question: question(nonProxyTitleWork, nonProxyDescriptionWork),
      when: [rules.proxyNo, rules.mainJob],
    },
    {
      question: question(proxyTitleWork, proxyDescriptionWork),
      when: [rules.proxyYes, rules.mainJob],
    },
    {
      question: question(pastNonProxyTitleWork, nonProxyDescriptionWork),
      when: [rules.proxyNo],
    },
    {
      question: question(pastProxyTitleWork, proxyDescriptionWork),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        group: 'submit-group',
      },
    },
  ],
}
