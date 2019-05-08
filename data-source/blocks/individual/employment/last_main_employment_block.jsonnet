local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

{
  type: 'Interstitial',
  id: 'last-main-employment-block',
  title: 'Last main job',
  content_variants: [
    {
      content: [
        {
          description: 'The next set of questions is about your last main job. Your main job is the job in which you usually worked the most hours',
        },
      ],
      when: [rules.proxyNo],
    },
    {
      content: [
        {
          description: {
            text: 'The next set of questions is about <em>{person_name_possessive}</em> last main job. Their main job is the job in which they usually worked the most hours',
            placeholders: [placeholders.personNamePossessive],
          },
        },
      ],
      when: [rules.proxyYes],
    },
  ],
}
