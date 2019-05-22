local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'establishment-position-question',
  title: title,
  definitions: [
    {
      title: 'What is an establishment?',
      content: [
        {
          description: 'A communal establishment is an establishment providing managed residential accommodation. ‘Managed’ in this context means full-time or part-time supervision of the accommodation. Examples of communal establishments include student halls of residence, boarding schools, armed forces bases, hospitals, care homes and prisons',
        },
      ],
    },
  ],
  type: 'General',
  answers: [
    {
      id: 'establishment-position-answer',
      mandatory: true,
      options: [
        {
          label: 'Resident',
          value: 'Resident',
          description: 'For example, student, member of Armed Forces, patient, detainee',
        },
        {
          label: 'Staff or owner',
          value: 'Staff or owner',
        },
        {
          label: 'Family member or partner of staff or owner',
          value: 'Family member or partner of staff or owner',
        },
        {
          label: 'Staying temporarily',
          value: 'Staying temporarily',
          description: 'No usual UK address',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'What is your position in this establishment?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> position in this establishment?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'establishment-position',
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
