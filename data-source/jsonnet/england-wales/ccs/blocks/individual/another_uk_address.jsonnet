local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'Is there another UK address where you may have been included on a census questionnaire because you were a usual resident, or staying overnight there on Sunday 13 October 2019?';
local proxyTitle = {
  text: 'Is there another UK address where {person_name} may have been included on a census questionnaire because they were a usual resident, or staying overnight there on Sunday 13 October 2019?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'another-uk-address',
  title: title,
  instruction: 'Tell respondent to turn to <strong>Showcard 12</strong>',
  type: 'MutuallyExclusive',
  mandatory: false,
  answers: [
    {
      id: 'another-uk-address-question',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'Previous home',
          value: 'Previous home',
          description: 'Moved since 13 October 2019',
        },
        {
          label: 'Armed forces base address',
          value: 'Armed forces base address',
        },
        {
          label: 'Another address when working away from home',
          value: 'Another address when working away from home',
        },
        {
          label: 'Student’s home address',
          value: 'Student’s home address',
        },
        {
          label: 'Student’s term-time address',
          value: 'Student’s term-time address',
        },
        {
          label: 'Another parent or guardian’s address',
          value: 'Another parent or guardian’s address',
        },
        {
          label: 'Partner’s address',
          value: 'Partner’s address',
        },
        {
          label: 'Holiday in the UK',
          value: 'Holiday in the UK',
        },
        {
          label: 'Other UK address',
          value: 'Other UK address',
        },
      ],
    },
    {
      id: 'another-uk-address-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'There is no other UK address',
          value: 'There is no other UK address',
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'another-uk-address',
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
        block: 'individual-section-summary',
        when: [{
          id: 'another-uk-address-question',
          condition: 'not set',
        }],
      },
    },
    {
      goto: {
        block: 'other-census-address',
      },
    },
  ],
}
