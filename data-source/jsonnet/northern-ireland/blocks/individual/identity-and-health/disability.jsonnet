local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'disability-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: false,
  answers: [
    {
      id: 'disability-answer',
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
          label: 'A mobility or dexterity difficulty, which requires the use of a wheelchair in the home',
          value: 'Full mobility',
        },
        {
          label: 'A mobility or dexterity difficulty that limits basic physical activities',
          value: 'Slight mobility',
          description: 'For example walking or dressing',
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
      id: 'disability-answer-exclusive',
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

local nonProxyTitle = 'Do you have any of the following <em>physical health conditions</em> which have lasted, or are expected to last, at least 12 months?';

local proxyTitle = {
  text: 'Does {person_name} have any of the following <em>physical health conditions</em> which have lasted, or are expected to last, at least 12 months?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'disability',
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
}
