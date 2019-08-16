local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description) = {
  title: title,
  id: 'study_location_type-question',
  description: description,
  type: 'General',
  answers: [
    {
      id: 'study_location_type-answer',
      mandatory: true,
      options: [
        {
          label: 'At a campus or school',
          value: 'At a campus or school',
        },
        {
          label: 'At or from home',
          value: 'At or from home',
        },
        {
          label: 'No fixed place',
          value: 'No fixed place',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitleStudy = 'Where do you mainly study?';
local proxyTitleStudy = {
  text: 'Where does <em>{person_name}</em> mainly study?',
  placeholders: [
    placeholders.personName,
  ],
};

local nonProxyDescriptionStudy = 'Answer for the place where you spend the most time. If student or schoolchild, answer for your study address.';
local proxyDescriptionStudy = 'Answer for the place where <em>{person_name}</em> spends the most time. If student or schoolchild, answer for their study address.';


{
  type: 'Question',
  id: 'study_location_type',
  question_variants: [
    {
      question: question(nonProxyTitleStudy, nonProxyDescriptionStudy),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitleStudy, proxyDescriptionStudy),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'school-location',
        when: [
          {
            id: 'study_location_type-answer',
            condition: 'equals',
            value: 'At a campus or school',
          },
        ],
      },
    },
    {
      goto: {
        group:'submit-group',
      },
    },
  ],
}
