const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const HouseholdMemberBegin = require('../../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../../pages/surveys/census/household/details-correct.page');
const Over16 = require('../../pages/surveys/census/household/over-16.page');
const PrivateResponse = require('../../pages/surveys/census/household/private-response.page');
const RequestPrivateResponse = require('../../pages/surveys/census/household/request-private-response.page');
const HouseholdMemberCompleted = require('../../pages/surveys/census/household/household-member-completed.page');


describe('Census Household', function () {

  it('Given I have added a householder, When I request a private response for that person, Then I don\'t have to complete any more questions for them', function () {
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
          .click(DetailsCorrect.yesThisIsMyFullName())
          .click(DetailsCorrect.submit())
          .click(Over16.yes())
          .click(Over16.submit())
          .click(PrivateResponse.yesIWantToRequestAPersonalForm())
          .click(PrivateResponse.submit())
          .click(RequestPrivateResponse.submit())
          .getUrl().should.eventually.contain(HouseholdMemberCompleted.pageName);
      });
  });

});
