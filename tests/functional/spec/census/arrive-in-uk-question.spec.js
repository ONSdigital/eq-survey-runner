const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const HouseholdMemberBegin = require('../../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../../pages/surveys/census/household/details-correct.page');
const Over16 = require('../../pages/surveys/census/household/over-16.page');
const CountryOfBirth = require('../../pages/surveys/census/household/country-of-birth.page');
const ArriveInUK = require('../../pages/surveys/census/household/arrive-in-uk.page');
const LengthOfStay = require('../../pages/surveys/census/household/length-of-stay.page');


describe('Census Household', function () {

  it('Given a census schema, When I select either/both of the bottom 2 options for Question - 9. What is your country of birth?, Then I should be displayed with ArriveInUk screen', function () {
    return helpers.startCensusQuestionnaire('census_household.json', false)
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
            return helpers.pressSubmit(7);
          })
          .then(() => {
          return browser
            .getUrl().should.eventually.contain(CountryOfBirth.pageName)
            .click(CountryOfBirth.englandRepublicOfIreland())
            .click(CountryOfBirth.submit())
            .getUrl().should.eventually.contain(ArriveInUK.pageName)

            .click(ArriveInUK.previous())
            .click(CountryOfBirth.englandOther())
            .click(CountryOfBirth.submit())
            .getUrl().should.eventually.contain(ArriveInUK.pageName)

            .click(ArriveInUK.previous())
            .click(CountryOfBirth.englandRepublicOfIreland())
            .click(CountryOfBirth.englandOther())
            .click(CountryOfBirth.submit())

            .getUrl().should.eventually.contain(ArriveInUK.pageName)
            .selectByValue(ArriveInUK.Month(), 5)
            .setValue(ArriveInUK.answerYear(), '1982')
            .click(ArriveInUK.submit())
            .getUrl().should.eventually.contain(LengthOfStay.pageName);
      });
    });
  });

});
