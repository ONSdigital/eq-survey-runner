const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const HouseholdMemberBegin = require('../../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../../pages/surveys/census/household/details-correct.page');
const Over16 = require('../../pages/surveys/census/household/over-16.page');
const EverWorked = require('../../pages/surveys/census/household/ever-worked.page');
const HouseholdMemberCompleted = require('../../pages/surveys/census/household/household-member-completed.page');


describe('Census Household', function () {
  it('Given I am answering question 33 Have you ever worked?, When I don\'t answer or answer No, Then i am routed to end end of the person', function () {
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
          .click(Over16.yes())
          .then(() => {
            return helpers.pressSubmit(25);
          })
          .then(() => {
          return browser
            .getUrl().should.eventually.contain(EverWorked.pageName)
            .click(EverWorked.submit())
            .getUrl().should.eventually.contain(HouseholdMemberCompleted.pageName)
            .click(HouseholdMemberCompleted.previous())
            .getUrl().should.eventually.contain(EverWorked.pageName)
            .click(EverWorked.no())
            .click(EverWorked.submit())
            .getUrl().should.eventually.contain(HouseholdMemberCompleted.pageName);
      });
    });
  });

});
