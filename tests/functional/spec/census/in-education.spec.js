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
const InEducation = require('../../pages/surveys/census/household/in-education.page');
const TermTimeLocation = require('../../pages/surveys/census/household/term-time-location.page');
const CountryOfBirth = require('../../pages/surveys/census/household/country-of-birth.page');
const HouseholdMemberCompleted = require('../../pages/surveys/census/household/household-member-completed.page');


describe('Census Household', function () {

  it('Given I am answering question 7 in the individual detail section - 7. Are you a schoolchild or student in full-time education?, When I do not select any response, Then I am routed to 9. What is your country of birth?', function () {
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
          .click(AnotherAddress.no())
          .click(AnotherAddress.submit())
          .click(InEducation.submit())
          .getUrl().should.eventually.contain(CountryOfBirth.pageName);
      });
  });

  it('Given I am answering 7. Are you a schoolchild or student in full-time education? and 8. ...do you live:, When I select -Yes- and here, at this address, Then I am routed to 9. Country of birth', function () {
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
          .click(AnotherAddress.no())
          .click(AnotherAddress.submit())
          .click(InEducation.yes())
          .click(InEducation.submit())
          .click(TermTimeLocation.hereAtThisAddress())
          .click(TermTimeLocation.submit())
          .getUrl().should.eventually.contain(CountryOfBirth.pageName);
      });
  });

  it('Given I am answering 7. Are you a schoolchild or student in full-time education? and 8. ...do you live:, When I select -Yes- and at another address, Then I am routed to end of person', function () {
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
          .click(AnotherAddress.no())
          .click(AnotherAddress.submit())
          .click(InEducation.yes())
          .click(InEducation.submit())
          .click(TermTimeLocation.atAnotherAddress())
          .click(TermTimeLocation.submit())
          .getUrl().should.eventually.contain(HouseholdMemberCompleted.pageName);
      });
  });

});
