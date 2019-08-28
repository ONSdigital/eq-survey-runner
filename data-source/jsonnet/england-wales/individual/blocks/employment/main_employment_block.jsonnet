local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

{
  type: 'Interstitial',
  id: 'main-employment-block',
  content_variants: [
    {
      content: {
        title: 'Main job',
        contents: [
          {
            description: 'The next set of questions is about your main job. Your main job is the job in which you usually work the most hours.',
          },
        ],
      },
      when: [rules.isNotProxy, rules.mainJob],
    },
    {
      content: {
        title: 'Main job',
        contents: [
          {
            description: {
              text: 'The next set of questions is about <em>{person_name_possessive}</em> main job. Their main job is the job in which they usually work the most hours.',
              placeholders: [placeholders.personNamePossessive],
            },
          },
        ],
      },
      when: [rules.isProxy, rules.mainJob],
    },
    {
      content: {
        title: 'Last main job',
        contents: [
          {
            description: 'The next set of questions is about your last main job. Your main job is the job in which you usually worked the most hours.',
          },
        ],
      },
      when: [rules.isNotProxy, rules.lastMainJob],
    },
    {
      content: {
        title: 'Last main job',
        contents: [
          {
            description: {
              text: 'The next set of questions is about <em>{person_name_possessive}</em> last main job. Their main job is the job in which they usually worked the most hours.',
              placeholders: [placeholders.personNamePossessive],
            },
          },
        ],
      },
      when: [rules.isProxy, rules.lastMainJob],
    },
  ],
}
