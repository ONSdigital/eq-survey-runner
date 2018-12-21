import {openQuestionnaire} from ../../../helpers/helpers.js

const PrimaryNameBlockPage = require('../../../generated_pages/answer_summary/primary-name-block.page.js');
const PrimaryAnyoneElseBlockPage = require('../../../generated_pages/answer_summary/primary-anyone-else-block.page.js');
const RepeatingNameBlockPage = require('../../../generated_pages/answer_summary/repeating-name-block.page.js');
const RepeatingAnyoneElseBlockPage = require('../../../generated_pages/answer_summary/repeating-anyone-else-block.page.js');
const HouseholdSummaryPage = require('../../../generated_pages/answer_summary/household-summary.page.js');

describe('Answer Summary', function () {

  describe('Given I enter my household composition, ', function () {
    before('load and display the form', function() {
      return helpers.openQuestionnaire('test_answer_summary.json')
        .then(() => {
                      .get(PrimaryNameBlockPage.primaryFirstName()).type('Bob')
            .get(PrimaryNameBlockPage.primaryLastName()).type('Smith')
            .get(PrimaryNameBlockPage.submit()).click()

            .get(PrimaryAnyoneElseBlockPage.yes()).click()
            .get(PrimaryAnyoneElseBlockPage.submit()).click()

            .get(RepeatingNameBlockPage.repeatingFirstName()).type('Sal')
            .get(RepeatingNameBlockPage.repeatingLastName()).type('Smith')
            .get(RepeatingNameBlockPage.submit()).click()

            .get(RepeatingAnyoneElseBlockPage.yes()).click()
            .get(RepeatingAnyoneElseBlockPage.submit()).click()

            .get(RepeatingNameBlockPage.repeatingFirstName()).type('Jill')
            .get(RepeatingNameBlockPage.repeatingLastName()).type('Smith')
            .get(RepeatingNameBlockPage.submit()).click()

            .get(RepeatingAnyoneElseBlockPage.no()).click()
            .get(RepeatingAnyoneElseBlockPage.submit()).click()

            .url().should('contain', HouseholdSummaryPage.pageName);
        });
    });


      it('When I view the Summary, Then the household members should be shown correctly', function () {
                  .get(HouseholdSummaryPage.primaryFirstNameLabel(1)).stripText().should('contain', 'Bob Smith')
          .get(HouseholdSummaryPage.repeatingFirstNameLabel(2)).stripText().should('contain', 'Sal Smith')
          .get(HouseholdSummaryPage.repeatingFirstNameLabel(3)).stripText().should('contain', 'Jill Smith');
      });

      it('When I click edit on primary person, Then I should be able to edit the answer and return to the summary', function () {
                  .get(HouseholdSummaryPage.primaryFirstNameEdit(1)).click()
          .url().should('contain', PrimaryNameBlockPage.pageName)
          .get(PrimaryNameBlockPage.primaryFirstName()).invoke('val').should('contain', 'Bob')
          .get(PrimaryNameBlockPage.primaryFirstName()).type('Robert')
          .get(PrimaryNameBlockPage.submit()).click()
          .url().should('contain', HouseholdSummaryPage.pageName)
          .get(HouseholdSummaryPage.primaryFirstNameLabel(1)).stripText().should('contain', 'Robert Smith');
      });

      it('When I click edit on first repeating person, Then I should be able to edit the answer and return to the summary', function () {
                  .get(HouseholdSummaryPage.repeatingFirstNameEdit(2)).click()
          .url().should('contain', RepeatingNameBlockPage.pageName)
          .get(RepeatingNameBlockPage.repeatingFirstName()).invoke('val').should('contain', 'Sal')
          .get(RepeatingNameBlockPage.repeatingFirstName()).type('Sally')
          .get(RepeatingNameBlockPage.submit()).click()
          .url().should('contain', HouseholdSummaryPage.pageName)
          .get(HouseholdSummaryPage.repeatingFirstNameLabel(2)).stripText().should('contain', 'Sally Smith');
      });

      it('When I click edit on second repeating person, Then I should be able to edit the answer and return to the summary', function () {
                  .get(HouseholdSummaryPage.repeatingFirstNameEdit(3)).click()
          .url().should('contain', RepeatingNameBlockPage.pageName)
          .get(RepeatingNameBlockPage.repeatingFirstName()).invoke('val').should('contain', 'Jill')
          .get(RepeatingNameBlockPage.repeatingFirstName()).type('Jillian')
          .get(RepeatingNameBlockPage.submit()).click()
          .url().should('contain', HouseholdSummaryPage.pageName)
          .get(HouseholdSummaryPage.repeatingFirstNameLabel(3)).stripText().should('contain', 'Jillian Smith');
      });

      it('When I click add person link, Then I should go to the anyone else page and be able to add additional people', function () {
                  .get(HouseholdSummaryPage.addPersonLink()).click()
          .url().should('contain', RepeatingAnyoneElseBlockPage.pageName)
          .get(RepeatingAnyoneElseBlockPage.yes()).click()
          .get(RepeatingAnyoneElseBlockPage.submit()).click()

          .get(RepeatingNameBlockPage.repeatingFirstName()).type('Dave')
          .get(RepeatingNameBlockPage.repeatingLastName()).type('Smith')
          .get(RepeatingNameBlockPage.submit()).click()
          .get(RepeatingAnyoneElseBlockPage.no()).click()
          .get(RepeatingAnyoneElseBlockPage.submit()).click()

          .url().should('contain', HouseholdSummaryPage.pageName)
          .get(HouseholdSummaryPage.repeatingFirstNameLabel(4)).stripText().should('contain', 'Dave Smith');
      });
  });
});
