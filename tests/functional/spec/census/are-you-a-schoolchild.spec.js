const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const HouseholdMemberBegin = require('../../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../../pages/surveys/census/household/details-correct.page');
const Over16 = require('../../pages/surveys/census/household/over-16.page');
const InEducation = require('../../pages/surveys/census/household/in-education.page');
const CountryOfBirth = require('../../pages/surveys/census/household/country-of-birth.page');

describe('Census Household', function () {

  it('Given I am answering question 7 in the individual detail section - 7. Are you a schoolchild or student in full-time education?, When I do not select any response or select no, Then I am routed to 9. What is your country of birth?', function () {
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
          .click(Over16.no())
          .then(() => {
            return helpers.pressSubmit(5);
          })
          .then(() => {
          return browser
            .getUrl().should.eventually.contain(InEducation.pageName)
            .click(InEducation.submit())
            .getUrl().should.eventually.contain(CountryOfBirth.pageName)
            .click(CountryOfBirth.previous())
            .click(InEducation.no())
            .click(InEducation.submit())
            .getUrl().should.eventually.contain(CountryOfBirth.pageName);
      });
    });
  });

});
