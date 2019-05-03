local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

{
  type: 'Interstitial',
  id: 'qualifications',
  title: 'Qualifications',
  content_variants: [
    {
      content: [
        {
          title: 'Qualifications',
          description: 'The next set of questions is about any qualifications you have ever achieved in England, Wales or worldwide, including equivalents, even if you are not using them now.',
        },
      ],
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      content: [
        {
          title: 'Qualifications',
          description: 'The next set of questions is about any qualifications you have ever achieved in Wales, England or worldwide, including equivalents, even if you are not using them now.',
        },
      ],
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      content: [
        {
          title: 'Qualifications',
          description: {
            text: 'The next set of questions is about any qualifications <em>{person_name}</em>, has ever achieved in England, Wales or worldwide, including equivalents, even if they are not using them now.',
            placeholders: [placeholders.personName],
          },
        },
      ],
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      content: [
        {
          title: 'Qualifications',
          description: {
            text: 'The next set of questions is about any qualifications <em>{person_name}</em>, has ever achieved in Wales, England or worldwide, including equivalents, even if they are not using them now.',
            placeholders: [placeholders.personName],
          },
        },
      ],
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
}
