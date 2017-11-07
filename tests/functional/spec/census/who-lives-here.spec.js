const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const ElsePermanentOrFamilyHome = require('../../pages/surveys/census/household/else-permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const EveryoneAtAddressConfirmation = require('../../pages/surveys/census/household/everyone-at-address-confirmation.page');
const OvernightVisitors = require('../../pages/surveys/census/household/overnight-visitors.page');

describe('Census Household', function () {

  it('Given I am answering question 1a in the who lives here section, When I select -Someone...- as the response, Then I am routed to Who lives here question 2', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.no())
          .click(PermanentOrFamilyHome.submit())
          .click(ElsePermanentOrFamilyHome.someoneLivesHereAsTheirPermanentHome())
          .click(ElsePermanentOrFamilyHome.submit())
          .getUrl().should.eventually.contain(HouseholdComposition.pageName);
      });
  });

  it('Given I am answering question 1a in the who lives here section, When I select -No One...- as the response, Then I am routed to Who lives here question 4', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.no())
          .click(PermanentOrFamilyHome.submit())
          .click(ElsePermanentOrFamilyHome.noOneLivesHereAsTheirPermanentHome())
          .click(ElsePermanentOrFamilyHome.submit())
          .getUrl().should.eventually.contain(OvernightVisitors.pageName);
      });
  });

  it('Given I am answering question 3 in the who lives here section, When I select -no- as the response, Then I am routed back to Who lives here question 2', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(EveryoneAtAddressConfirmation.noINeedToAddAnotherPerson())
          .click(EveryoneAtAddressConfirmation.submit())
          .getUrl().should.eventually.contain(HouseholdComposition.pageName);
      });
  });


  it('Given I am answering question 3 in the who lives here section, When I don\'t select a response, Then I am routed to Who lives here question 4', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(EveryoneAtAddressConfirmation.submit())
          .getUrl().should.eventually.contain(OvernightVisitors.pageName);
      });
  });



});
