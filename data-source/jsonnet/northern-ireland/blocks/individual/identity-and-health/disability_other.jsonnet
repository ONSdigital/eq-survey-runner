local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title) = {
  id: 'disability-other-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: true,
  answers: [
    {
      id: 'disability-other-answer',
      mandatory: false,
      options: [
        {
          label: 'Deafness or partial hearing loss',
          value: 'Deafness or partial hearing loss',
        },
        {
          label: 'Blindness or partial sight loss',
          value: 'Blindness or partial sight loss',
        },
        {
          label: 'A mobility or dexterity difficulty that limits basic physical activities',
          value: 'Slight mobility',
          description: 'For example walking or dressing',
        },
        {
          label: 'A mobility or dexterity difficulty, which requires the use of a wheelchair in the home',
          value: 'Full mobility',
        },
        {
          label: 'Shortness of breath or difficulty breathing',
          value: 'Shortness of breath or difficulty breathing',
          description: 'For example Asthma',
        },
      ],
      type: 'Checkbox',
    },
    {
      id: 'disability-other-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'None of these conditions',
          value: 'None of these conditions',
        },
      ],
    },
  ],
};

local nonProxyTitle = 'Do you have any of the following other health conditions or illnesses lasting or expected to last 12 months or more?';

local proxyTitle = {
  text: 'Does <em>{person_name}</em> have any of the following other health conditions or illnesses lasting or expected to last 12 months or more?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'disability-other',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle),
      when: [rules.proxyYes],
    },
  ],
}
