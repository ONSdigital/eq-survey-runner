local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local descriptionNonProxy = 'The next set of questions is about the qualifications you have achieved in Northern Ireland or worldwide, even if you are not using them now.';
local descriptionProxy = 'The next set of questions is about the qualifications <em>{person_name}</em> has achieved in Northern Ireland or worldwide, even if they are not using them now.';

{
  type: 'Interstitial',
  id: 'qualifications',
  content_variants: [
    {
      content: {
        title: 'Qualifications',
        contents: [
          {
            description: descriptionNonProxy,
          },
        ],
      },
      when: [rules.isNotProxy],
    },
    {
      content: {
        title: 'Qualifications',
        contents: [
          {
            description: {
              text: descriptionProxy,
              placeholders: [placeholders.personName],
            },
          },
        ],
      },
      when: [rules.isProxy],
    },
  ],
}
