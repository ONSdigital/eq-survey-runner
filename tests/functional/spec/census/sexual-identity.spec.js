const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const HouseholdMemberBegin = require('../../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../../pages/surveys/census/household/details-correct.page');
const Over16 = require('../../pages/surveys/census/household/over-16.page');
const SexualIdentity = require('../../pages/surveys/census/household/sexual-identity.page');
const Language = require('../../pages/surveys/census/household/language.page');

describe('Census Household', function () {
  it('Given Respondent Home has set the sexual identity flag and I have chosen over 16, When I complete the EQ, Then I should be asked the sexual id question', function () {
    return helpers.startCensusQuestionnaire('census_household.json', true)
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(helpers.navigationLink('John'))
          .click(HouseholdMemberBegin.submit())
          .click(DetailsCorrect.submit())
          .click(Over16.yes())
          .then(() => {
            return helpers.pressSubmit(13);
          })
          .then(() => {
          return browser
            .getUrl().should.eventually.contain(SexualIdentity.pageName)
            .click(SexualIdentity.heterosexualOrStraight())
            .click(SexualIdentity.submit())
            .getUrl().should.eventually.contain(Language.pageName);
      });
    });
  });

  it('Given Respondent Home has set the sexual identity flag and I have chosen under 16, When I complete the EQ, Then I should not be asked the sexual id question', function () {
    return helpers.startCensusQuestionnaire('census_household.json', true)
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(helpers.navigationLink('John'))
          .click(HouseholdMemberBegin.submit())
          .click(DetailsCorrect.submit())
          .click(Over16.no())
          .then(() => {
            return helpers.pressSubmit(12);
          })
          .then(() => {
          return browser
            .getUrl().should.eventually.contain(Language.pageName);
      });
    });
  });
});
