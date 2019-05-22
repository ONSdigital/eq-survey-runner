local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local descriptionNonProxy = 'The next set of questions is about the qualifications you have ever acheived in Northern Ireland or worldwide, even if you are not using them now.';
local descriptionProxy = 'The next set of questions is about the qualifications <em>{person_name}</em> has ever acheived in Northern Ireland or worldwide, even if they are not using them now.';

{
  type: 'Interstitial',
  id: 'qualifications',
  title: 'Qualifications',
  content_variants: [
    {
      content: [
        {
          description: descriptionNonProxy,
        },
      ],
      when: [rules.proxyNo],
    },
    {
      content: [
        {
          description: {
            text: descriptionProxy,
            placeholders: [placeholders.personName],
          },
        },
      ],
      when: [rules.proxyYes],
    },
  ],
}
