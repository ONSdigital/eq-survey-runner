local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

{
  type: 'Interstitial',
  id: 'main-employment-block',
  title: '',
  content_variants: [
    {
      content: [
        {
          title: 'Answer the next set of questions for your main job',
          description: 'Your main job is the job in which you usually work the most hours',
        },
      ],
      when: [rules.proxyNo, rules.mainJob],
    },
    {
      content: [
        {
          title: {
            text: 'Answer the next set of questions for {person_name_possessive} main job',
            placeholders: [placeholders.personNamePossessive],
          },
          description: 'Their main job is the job in which they usually work the most hours',
        },
      ],
      when: [rules.proxyYes, rules.mainJob],
    },
    {
      content: [
        {
          title: 'Answer the next set of questions for your last main job',
          description: 'Your main job is the job in which you usually worked the most hours',
        },
      ],
      when: [rules.proxyNo, rules.lastMainJob],
    },
    {
      content: [
        {
          title: {
            text: 'Answer the next set of questions for {person_name_possessive} last main job',
            placeholders: [placeholders.personNamePossessive],
          },
          description: 'Their main job is the job in which they usually worked the most hours',
        },
      ],
      when: [rules.proxyYes, rules.lastMainJob],
    },
  ],
}
