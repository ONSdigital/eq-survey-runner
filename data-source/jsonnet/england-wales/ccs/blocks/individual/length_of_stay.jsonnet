local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'length-of-stay-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'length-of-stay-answer',
      mandatory: false,
      options: [
        {
          label: 'Less than 12 months',
          value: 'Less than 12 months',
        },
        {
          label: '12 months or more',
          value: '12 months or more',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Including the time you have already spent here, how long do you intend to stay in the United Kingdom?';

local proxyTitle = {
  text: 'Including the time they have already spent here, how long does {person_name} intend to stay in the United Kingdom?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'length-of-stay',
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
        block: 'employment-status',
        when: [
          rules.over16,
        ],
      },
    },
    {
      goto: {
        block: 'employment-status',
        when: [
          rules.estimatedAge,
        ],
      },
    },
    {
      goto: {
        block: 'another-uk-address',
      },
    },
  ],
}
