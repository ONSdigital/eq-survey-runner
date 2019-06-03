local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local englandDescriptionNonProxy = 'The next set of questions is about any qualifications you have ever achieved in England, Wales or worldwide, including equivalents, even if you are not using them now.';
local englandDescriptionProxy = 'The next set of questions is about any qualifications <em>{person_name}</em> has ever achieved in England, Wales or worldwide, including equivalents, even if they are not using them now.';

local walesDescriptionNonProxy = 'The next set of questions is about any qualifications you have ever achieved in Wales, England or worldwide, including equivalents, even if you are not using them now.';
local walesDescriptionProxy = 'The next set of questions is about any qualifications <em>{person_name}</em> has ever achieved in Wales, England or worldwide, including equivalents, even if they are not using them now.';

function(region_code) (
  local regionDescriptionNonProxy = if region_code == 'GB-WLS' then walesDescriptionNonProxy else englandDescriptionNonProxy;
  local regionDescriptionProxy = if region_code == 'GB-WLS' then walesDescriptionProxy else englandDescriptionProxy;
  {
    type: 'Interstitial',
    id: 'qualifications',
    title: 'Qualifications',
    content_variants: [
      {
        content: [
          {
            description: regionDescriptionNonProxy,
          },
        ],
        when: [rules.proxyNo],
      },
      {
        content: [
          {
            description: {
              text: regionDescriptionProxy,
              placeholders: [placeholders.personName],
            },
          },
        ],
        when: [rules.proxyYes],
      },
    ],
  }
)
