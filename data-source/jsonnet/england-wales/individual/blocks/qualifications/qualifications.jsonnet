local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

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
    content_variants: [
      {
        content: {
          title: 'Qualifications',
          contents: [
            {
              description: regionDescriptionNonProxy,
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
                text: regionDescriptionProxy,
                placeholders: [placeholders.personName],
              },
            },
          ],
        },
        when: [rules.isProxy],
      },
    ],
  }
)
