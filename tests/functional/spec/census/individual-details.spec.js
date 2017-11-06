const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const HouseholdMemberBegin = require('../../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../../pages/surveys/census/household/details-correct.page');
const CorrectName = require('../../pages/surveys/census/household/correct-name.page');
const Over16 = require('../../pages/surveys/census/household/over-16.page');

describe('Census Household', function () {

  it('Given I am answering question 1 in the individual detail section, When I select -no- as response, Then I am routed to What is your correct name question 1a ', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
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
          .click(DetailsCorrect.noINeedToChangeMyName())
          .click(DetailsCorrect.submit())
          .setValue(CorrectName.correctFirstName(), 'Dave')
          .click(CorrectName.submit())
          .getUrl().should.eventually.contain(Over16.pageName);
      });
  });

  it('Given I am answering question 1 in the individual detail section, When I do not select any response, Then I am routed to Are you over 16', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
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
          .getUrl().should.eventually.contain(Over16.pageName);
      });
  });
});
