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
          title: 'The next set of questions is about your qualifications',
          description: 'Record any qualifications you have ever achieved in England, Wales or worldwide, including equivalents, even if you are not using them now.',
        },
      ],
      when: [rules.proxyNo],
    },
    {
      content: [
        {
          title: {
            text: 'The next set of questions is about {person_name_possessive} qualifications',
            placeholders: [placeholders.personNamePossessive],
          },
          description: 'Record any qualifications they have ever achieved in England, Wales or worldwide, including equivalents, even if they are not using them now.',
        },
      ],
      when: [rules.proxyYes],
    },
  ],
}
