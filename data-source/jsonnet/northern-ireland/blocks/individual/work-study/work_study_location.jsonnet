local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description, firstRadioLabel) = {
  title: title,
  id: 'work-study-location-question',
  description: description,
  type: 'General',
  answers: [
    {
      id: 'work-study-location-answer',
      mandatory: true,
      options: [
        {
          label: firstRadioLabel,
          value: firstRadioLabel,
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
local nonProxyTitleWork = 'Where do you mainly work?';
local proxyTitleWork = {
  text: 'Where does <em>{person_name}</em> mainly work?',
  placeholders: [
    placeholders.personName,
  ],
};
local nonProxyTitleDidWork = 'Where did you mainly work?';
local proxyTitleDidWork = {
  text: 'Where did <em>{person_name}</em> mainly work?',
  placeholders: [
    placeholders.personName,
  ],
};

local nonProxyDescriptionStudy = 'Answer for the place where you spend the most time. If student or schoolchild, answer for your study address.';
local proxyDescriptionStudy = 'Answer for the place where <em>{person_name}</em> spends the most time. If student or schoolchild, answer for their study address.';
local nonProxyDescriptionWork = 'Answer for the place where you spend the most time. If working (even if ill, on maternity leave, holiday or temporarily laid off) provide your main work address.';
local proxyDescriptionWork = 'Answer for the place where <em>{person_name}</em> spends the most time. If working (even if ill, on maternity leave, holiday or temporarily laid off) provide their main work address.';
local nonProxyDescriptionDidWork = 'Answer for the place where you spent the most time.';
local proxyDescriptionDidWork = 'Answer for the place where <em>{person_name}</em> spent the most time.';

local firstRadioStudy = 'At a campus or school';
local firstRadioWork = 'At a workplace';


{
  type: 'Question',
  id: 'work-study-location',
  question_variants: [
    {
      question: question(nonProxyTitleStudy, nonProxyDescriptionStudy, firstRadioStudy),
      when: [rules.proxyNo, rules.hasNotWorked],
    },
    {
      question: question(proxyTitleStudy, proxyDescriptionStudy, firstRadioStudy),
      when: [rules.proxyYes, rules.hasNotWorked],
    },
    {
      question: question(nonProxyTitleWork, nonProxyDescriptionWork, firstRadioWork),
      when: [rules.proxyNo, rules.working],
    },
    {
      question: question(proxyTitleWork, proxyDescriptionWork, firstRadioWork),
      when: [rules.proxyYes, rules.working],
    },
    {
      question: question(nonProxyTitleDidWork, nonProxyDescriptionDidWork, firstRadioWork),
      when: [rules.proxyNo, rules.working],
    },
    {
      question: question(proxyTitleDidWork, proxyDescriptionDidWork, firstRadioWork,
      when: [rules.proxyYes, rules.working],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'school-location',
        when: [
          rules.hasNotWorked,
          {
            id: 'work-study-location-answer',
            condition: 'equals',
            value: 'At a campus or school',
          },
        ],
      },
      goto: {
        block: 'work-location',
        when: [
          rules.working,
          {
            id: 'work-study-location-answer',
            condition: 'equals',
            value: 'At a workplace',
          },
        ],
      },
    },
    {
      goto: {
        block:'submit-answers-section',
      },
    },
  ],
}
