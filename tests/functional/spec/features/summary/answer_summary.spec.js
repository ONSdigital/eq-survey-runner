const helpers = require('../../../helpers');

const PrimaryNameBlockPage = require('../../../pages/surveys/answer_summary/primary-name-block.page.js');
const PrimaryAnyoneElseBlockPage = require('../../../pages/surveys/answer_summary/primary-anyone-else-block.page.js');
const RepeatingNameBlockPage = require('../../../pages/surveys/answer_summary/repeating-name-block.page.js');
const RepeatingAnyoneElseBlockPage = require('../../../pages/surveys/answer_summary/repeating-anyone-else-block.page.js');
const HouseholdSummaryPage = require('../../../pages/surveys/answer_summary/household-summary.page.js');

describe('Answer Summary', function () {

  describe('Given I enter my household composition, ', function () {
    before('load and display the form', function() {
      return helpers.openQuestionnaire('test_answer_summary.json')
        .then(() => {
          return browser
            .setValue(PrimaryNameBlockPage.primaryFirstName(), 'Bob')
            .setValue(PrimaryNameBlockPage.primaryLastName(), 'Smith')
            .click(PrimaryNameBlockPage.submit())

            .click(PrimaryAnyoneElseBlockPage.yes())
            .click(PrimaryAnyoneElseBlockPage.submit())

            .setValue(RepeatingNameBlockPage.repeatingFirstName(), 'Sal')
            .setValue(RepeatingNameBlockPage.repeatingLastName(), 'Smith')
            .click(RepeatingNameBlockPage.submit())

            .click(RepeatingAnyoneElseBlockPage.yes())
            .click(RepeatingAnyoneElseBlockPage.submit())

            .setValue(RepeatingNameBlockPage.repeatingFirstName(), 'Jill')
            .setValue(RepeatingNameBlockPage.repeatingLastName(), 'Smith')
            .click(RepeatingNameBlockPage.submit())

            .click(RepeatingAnyoneElseBlockPage.no())
            .click(RepeatingAnyoneElseBlockPage.submit())

            .getUrl().should.eventually.contain(HouseholdSummaryPage.pageName);
        });
    });


      it('When I view the Summary, Then the household members should be shown correctly', function () {
        return browser
          .getText(HouseholdSummaryPage.primaryFirstNameLabel(1)).should.eventually.contain('Bob Smith')
          .getText(HouseholdSummaryPage.repeatingFirstNameLabel(2)).should.eventually.contain('Sal Smith')
          .getText(HouseholdSummaryPage.repeatingFirstNameLabel(3)).should.eventually.contain('Jill Smith');
      });

      it('When I click edit on primary person, Then I should be able to edit the answer and return to the summary', function () {
        return browser
          .click(HouseholdSummaryPage.primaryFirstNameEdit(1))
          .getUrl().should.eventually.contain(PrimaryNameBlockPage.pageName)
          .getValue(PrimaryNameBlockPage.primaryFirstName()).should.eventually.contain('Bob')
          .setValue(PrimaryNameBlockPage.primaryFirstName(), 'Robert')
          .click(PrimaryNameBlockPage.submit())
          .getUrl().should.eventually.contain(HouseholdSummaryPage.pageName)
          .getText(HouseholdSummaryPage.primaryFirstNameLabel(1)).should.eventually.contain('Robert Smith');
      });

      it('When I click edit on first repeating person, Then I should be able to edit the answer and return to the summary', function () {
        return browser
          .click(HouseholdSummaryPage.repeatingFirstNameEdit(2))
          .getUrl().should.eventually.contain(RepeatingNameBlockPage.pageName)
          .getValue(RepeatingNameBlockPage.repeatingFirstName()).should.eventually.contain('Sal')
          .setValue(RepeatingNameBlockPage.repeatingFirstName(), 'Sally')
          .click(RepeatingNameBlockPage.submit())
          .getUrl().should.eventually.contain(HouseholdSummaryPage.pageName)
          .getText(HouseholdSummaryPage.repeatingFirstNameLabel(2)).should.eventually.contain('Sally Smith');
      });

      it('When I click edit on second repeating person, Then I should be able to edit the answer and return to the summary', function () {
        return browser
          .click(HouseholdSummaryPage.repeatingFirstNameEdit(3))
          .getUrl().should.eventually.contain(RepeatingNameBlockPage.pageName)
          .getValue(RepeatingNameBlockPage.repeatingFirstName()).should.eventually.contain('Jill')
          .setValue(RepeatingNameBlockPage.repeatingFirstName(), 'Jillian')
          .click(RepeatingNameBlockPage.submit())
          .getUrl().should.eventually.contain(HouseholdSummaryPage.pageName)
          .getText(HouseholdSummaryPage.repeatingFirstNameLabel(3)).should.eventually.contain('Jillian Smith');
      });

      it('When I click add person link, Then I should go to the anyone else page and be able to add additional people', function () {
        return browser
          .click(HouseholdSummaryPage.addPersonLink())
          .getUrl().should.eventually.contain(RepeatingAnyoneElseBlockPage.pageName)
          .click(RepeatingAnyoneElseBlockPage.yes())
          .click(RepeatingAnyoneElseBlockPage.submit())

          .setValue(RepeatingNameBlockPage.repeatingFirstName(), 'Dave')
          .setValue(RepeatingNameBlockPage.repeatingLastName(), 'Smith')
          .click(RepeatingNameBlockPage.submit())
          .click(RepeatingAnyoneElseBlockPage.no())
          .click(RepeatingAnyoneElseBlockPage.submit())

          .getUrl().should.eventually.contain(HouseholdSummaryPage.pageName)
          .getText(HouseholdSummaryPage.repeatingFirstNameLabel(4)).should.eventually.contain('Dave Smith');
      });
  });
});
