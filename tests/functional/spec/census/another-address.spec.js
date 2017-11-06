const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const HouseholdMemberBegin = require('../../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../../pages/surveys/census/household/details-correct.page');
const Over16 = require('../../pages/surveys/census/household/over-16.page');
const PrivateResponse = require('../../pages/surveys/census/household/private-response.page');
const Sex = require('../../pages/surveys/census/household/sex.page');
const DateOfBirth = require('../../pages/surveys/census/household/date-of-birth.page');
const MaritalStatus = require('../../pages/surveys/census/household/marital-status.page');
const AnotherAddress = require('../../pages/surveys/census/household/another-address.page');
const OtherAddress = require('../../pages/surveys/census/household/other-address.page');
const AddressType = require('../../pages/surveys/census/household/address-type.page');
const InEducation = require('../../pages/surveys/census/household/in-education.page');


describe('Census Household', function () {

  it('Given I am answering question 5 in the individual detail section -Do you stay at another address for more than 30 days a year?, When I select -Yes, an address within the UK- as response, Then I am routed to 5a. Enter details of the other UK address where you stay more than 30 days a year?', function () {
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
          .click(PrivateResponse.noIDoNotWantToRequestAPersonalForm())
          .click(PrivateResponse.submit())
          .click(Sex.male())
          .click(Sex.submit())
          .setValue(DateOfBirth.day(), 2)
          .selectByValue(DateOfBirth.month(), 4)
          .setValue(DateOfBirth.year(), 1980)
          .click(DateOfBirth.submit())
          .click(MaritalStatus.married())
          .click(MaritalStatus.submit())
          .click(AnotherAddress.yesAnAddressWithinTheUk())
          .click(AnotherAddress.submit())
          .setValue(OtherAddress.building(), '101')
          .setValue(OtherAddress.street(), 'High Street')
          .setValue(OtherAddress.city(), 'New Town')
          .setValue(OtherAddress.postcode(), 'AB12 3CD')
          .click(OtherAddress.submit())
          .click(AddressType.anotherAddressWhenWorkingAwayFromHome())
          .click(AddressType.submit())
          .getUrl().should.eventually.contain(InEducation.pageName);
      });
  });

  it('Given I am answering question 5 in the individual detail section -Do you stay at another address for more than 30 days a year?, When I select -Yes, an address outside the UK, Then I am routed to 6. What is that address?', function () {
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
          .click(PrivateResponse.noIDoNotWantToRequestAPersonalForm())
          .click(PrivateResponse.submit())
          .click(Sex.male())
          .click(Sex.submit())
          .setValue(DateOfBirth.day(), 2)
          .selectByValue(DateOfBirth.month(), 4)
          .setValue(DateOfBirth.year(), 1980)
          .click(DateOfBirth.submit())
          .click(MaritalStatus.married())
          .click(MaritalStatus.submit())
          .click(AnotherAddress.other())
          .setValue(AnotherAddress.otherText(), 'SPAIN')
          .click(AnotherAddress.submit())
          .click(AddressType.holidayHome())
          .click(AddressType.submit())
          .getUrl().should.eventually.contain(InEducation.pageName);
      });
  });

  it('Given I am answering question 5 in the individual detail section -Do you stay at another address for more than 30 days a year?, When I dont select an answer, Then I am routed to 7. Are you a schoolchild or student in full-time education', function () {
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
          .click(PrivateResponse.noIDoNotWantToRequestAPersonalForm())
          .click(PrivateResponse.submit())
          .click(Sex.male())
          .click(Sex.submit())
          .setValue(DateOfBirth.day(), 2)
          .selectByValue(DateOfBirth.month(), 4)
          .setValue(DateOfBirth.year(), 1980)
          .click(DateOfBirth.submit())
          .click(MaritalStatus.married())
          .click(MaritalStatus.submit())
          .click(AnotherAddress.submit())
          .getUrl().should.eventually.contain(InEducation.pageName);
      });
  });


});
