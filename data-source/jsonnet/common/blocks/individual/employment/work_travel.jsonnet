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
      mandatory: true,
      options: [
        {
          label: 'Work mainly at or from home',
          value: 'Work mainly at or from home',
        },
        {
          label: 'Underground, metro, light rail or tram',
          value: 'Underground, metro, light rail or tram',
        },
        {
          label: 'Train',
          value: 'Train',
        },
        {
          label: 'Bus, minibus or coach',
          value: 'Bus, minibus or coach ',
        },
        {
          label: 'Taxi',
          value: 'Taxi ',
        },
        {
          label: 'Motorcycle, scooter or moped',
          value: 'Motorcycle, scooter or moped',
        },
        {
          label: 'Driving a car or van',
          value: 'Driving a car or van',
        },
        {
          label: 'Passenger in a car or van',
          value: 'Passenger in a car or van',
        },
        {
          label: 'Bicycle',
          value: 'Bicycle',
        },
        {
          label: 'On foot',
          value: 'On foot',
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

local nonProxyTitle = 'How do you usually travel to work?';
local nonProxyDescription = 'Answer for the longest part, by distance, of your usual journey to work';
local proxyTitle = {
  text: 'How does <em>{person_name}</em> usually travel to work?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyDescription = 'Answer for the longest part, by distance, of their usual journey to work';

{
  type: 'Question',
  id: 'work-travel',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDescription),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyDescription),
      when: [rules.proxyYes],
    },
  ],
}
