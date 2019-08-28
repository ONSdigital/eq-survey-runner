const helpers = require('../../helpers');

const DoYouLiveHereBlockPage = require('../../generated_pages/confirmation_question_within_repeating_section/primary-person-list-collector.page');
const AddPersonPage = require('../../generated_pages/confirmation_question_within_repeating_section/primary-person-list-collector-add.page');
const NumberOfEmployeesBreakdownBlockPage = require('../../generated_pages/confirmation_question_within_repeating_section/number-of-employees-split-block.page');
const NumberOfEmployeesTotalBlockPage = require('../../generated_pages/confirmation_question_within_repeating_section/number-of-employees-total-block.page');
const ConfirmZeroEmployeesBlockPage = require('../../generated_pages/confirmation_question_within_repeating_section/confirm-zero-employees-block.page');
const SummaryPage = require('../../generated_pages/confirmation_question_within_repeating_section/summary.page.js');

describe('Feature: Confirmation Question Within A Repeating Section', function () {

  describe('Given I am in a repeating section', function () {

    beforeEach('Add a person', function () {
      return helpers.openQuestionnaire('test_confirmation_question_within_repeating_section.json').then(() => {
        return browser
          .click(DoYouLiveHereBlockPage.yes())
          .click(DoYouLiveHereBlockPage.submit())
          .setValue(AddPersonPage.firstName(), 'John')
          .setValue(AddPersonPage.lastName(), 'Doe')
          .click(AddPersonPage.submit())
          .getUrl().should.eventually.contain(NumberOfEmployeesTotalBlockPage.url().split('/').slice(-1)[0]);
      });
    });

    describe('Given a confirmation question', function () {

      it('When I answer \'No\' to the confirmation question, Then I should be routed back to the source question', function () {
        return browser
          .click(NumberOfEmployeesTotalBlockPage.submit())
          .click(ConfirmZeroEmployeesBlockPage.no())
          .click(ConfirmZeroEmployeesBlockPage.submit())
          .getUrl().should.eventually.contain(NumberOfEmployeesTotalBlockPage.pageName);
      });

    });

    describe('Given I have answered a confirmation question', function () {

      it('When I view the summary, Then the confirmation question should not be displayed', function () {
        return browser
          .setValue(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal(), 0)
          .click(NumberOfEmployeesTotalBlockPage.submit())
          .click(ConfirmZeroEmployeesBlockPage.yes())
          .click(ConfirmZeroEmployeesBlockPage.submit())
          .getUrl().should.eventually.contain(SummaryPage.pageName)
          .isExisting(SummaryPage.confirmZeroEmployeesAnswer()).should.eventually.be.false;
      });

    });

    describe('Given a question with a skip condition', function () {

      it('When I submit an answer that is at least \'1\', Then I should be skipped past the confirmation question', function () {
        return browser
          .setValue(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal(), 3)
          .click(NumberOfEmployeesTotalBlockPage.submit())
          .getUrl().should.eventually.contain(NumberOfEmployeesBreakdownBlockPage.pageName)
          .getText(NumberOfEmployeesBreakdownBlockPage.questionText()).should.eventually.contain('Of the 3 total employees');
      });

    });

  });

});
