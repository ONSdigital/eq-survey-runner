const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const EveryoneAtAddressConfirmation = require('../../pages/surveys/census/household/everyone-at-address-confirmation.page');
const OvernightVisitors = require('../../pages/surveys/census/household/overnight-visitors.page');
const VisitorBegin = require('../../pages/surveys/census/household/visitor-begin.page');
const VisitorName = require('../../pages/surveys/census/household/visitor-name.page');
const VisitorSex = require('../../pages/surveys/census/household/visitor-sex.page');
const VisitorDateOfBirth = require('../../pages/surveys/census/household/visitor-date-of-birth.page');
const VisitorUkResident = require('../../pages/surveys/census/household/visitor-uk-resident.page');
const VisitorAddress = require('../../pages/surveys/census/household/visitor-address.page');
const VisitorCompleted = require('../../pages/surveys/census/household/visitor-completed.page');


describe('Census Household', function () {

  it('Given I have two visitors, When I complete the visitor details for person one, Then I should be asked visitor details for person two.', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(EveryoneAtAddressConfirmation.yes())
          .click(EveryoneAtAddressConfirmation.submit())
          .setValue(OvernightVisitors.answer(), 2)
          .click(OvernightVisitors.submit())
          .click(helpers.navigationLink('Visitors'))
          .click(VisitorBegin.submit())
          .setValue(VisitorName.visitorFirstName(), 'Jane')
          .setValue(VisitorName.visitorLastName(), 'Doe')
          .click(VisitorName.submit())
          .click(VisitorSex.female())
          .click(VisitorSex.submit())
          .setValue(VisitorDateOfBirth.day(), 10)
          .selectByValue(VisitorDateOfBirth.month(), 7)
          .setValue(VisitorDateOfBirth.year(), 1990)
          .click(VisitorDateOfBirth.submit())
          .click(VisitorUkResident.yesUsuallyLivesInTheUnitedKingdom())
          .click(VisitorUkResident.submit())
          .setValue(VisitorAddress.building(), 50)
          .setValue(VisitorAddress.street(), 'My Road')
          .setValue(VisitorAddress.city(), 'Newport')
          .setValue(VisitorAddress.postcode(), 'AB123CD')
          .click(VisitorAddress.submit())
          .click(VisitorCompleted.submit())
          .getUrl().should.eventually.contain(VisitorBegin.pageName);
      });
  });


  it('Given I have a visitor, When I they usually live outside of uk, Then I should have completed questions for that person.', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(EveryoneAtAddressConfirmation.yes())
          .click(EveryoneAtAddressConfirmation.submit())
          .setValue(OvernightVisitors.answer(), 1)
          .click(OvernightVisitors.submit())
          .click(helpers.navigationLink('Visitors'))
          .click(VisitorBegin.submit())
          .setValue(VisitorName.visitorFirstName(), 'Jane')
          .setValue(VisitorName.visitorLastName(), 'Doe')
          .click(VisitorName.submit())
          .click(VisitorSex.female())
          .click(VisitorSex.submit())
          .setValue(VisitorDateOfBirth.day(), 10)
          .selectByValue(VisitorDateOfBirth.month(), 7)
          .setValue(VisitorDateOfBirth.year(), 1990)
          .click(VisitorDateOfBirth.submit())
          .click(VisitorUkResident.other())
          .setValue(VisitorUkResident.otherText(), 'SPAIN')
          .click(VisitorAddress.submit())
          .getUrl().should.eventually.contain(VisitorCompleted.pageName);
      });
  });



});
