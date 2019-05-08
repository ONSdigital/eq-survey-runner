local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

{
  type: 'Interstitial',
  id: 'main-employment-block',
  title: 'Main job',
  content_variants: [
    {
      content: [
        {
          description: 'The next set of questions is about your main job. Your main job is the job in which you usually work the most hours',
        },
      ],
      when: [rules.proxyNo],
    },
    {
      content: [
        {
          description: {
            text: 'The next set of questions is about <em>{person_name_possessive}</em> main job. Their main job is the job in which they usually work the most hours',
            placeholders: [placeholders.personNamePossessive],
          },
        },
      ],
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'main-job-type',
      },
    },
  ],
}
