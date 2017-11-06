const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const EveryoneAtAddressConfirmation = require('../../pages/surveys/census/household/everyone-at-address-confirmation.page');

describe('Census Household', function () {

  it('Given I am answering question 1 in the individual detail section, When I select -no- as response, Then I am routed to What is your correct name question 1a ', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(),'Alpha')
          .setValue(HouseholdComposition.lastName(),'One')
          .click(HouseholdComposition.addPerson())
          .setValue(HouseholdComposition.firstName('_1'),'Bravo')
          .setValue(HouseholdComposition.lastName('_1'),'Two')
          .click(HouseholdComposition.submit())
          .isExisting(helpers.navigationLink('Alpha One')).should.eventually.be.true
          .isExisting(helpers.navigationLink('Bravo Two')).should.eventually.be.true
          .click(EveryoneAtAddressConfirmation.noINeedToAddAnotherPerson())
          .click(EveryoneAtAddressConfirmation.submit())
          .click(HouseholdComposition.removePerson(2))
          .waitUntil(function () {
          return browser.elements(HouseholdComposition.removePerson(2)).then(function (e) {
              return e.value.length === 0;
            });
          }, 2000, 'Person not removed in time')
          .click(HouseholdComposition.submit())
          .isExisting(helpers.navigationLink('Alpha One')).should.eventually.be.true
          .isExisting(helpers.navigationLink('Bravo Two')).should.eventually.be.false;
      });
  });

});
