const helpers = require('../../helpers');

const DoesAnyoneLiveHerePage = require('../../generated_pages/confirmation_question_within_repeating_section/list-collector.page');
const AddPersonPage = require('../../generated_pages/confirmation_question_within_repeating_section/list-collector-add.page');
const NumberOfEmployeesBreakdownPage = require('../../generated_pages/confirmation_question_within_repeating_section/number-of-employees-split-block.page');
const NumberOfEmployeesTotalPage = require('../../generated_pages/confirmation_question_within_repeating_section/number-of-employees-total-block.page');
const ConfirmZeroEmployeesPage = require('../../generated_pages/confirmation_question_within_repeating_section/confirm-zero-employees-block.page');
const SummaryPage = require('../../generated_pages/confirmation_question_within_repeating_section/summary.page.js');

describe('Feature: Confirmation Question Within A Repeating Section', function () {

  describe('Given I am in a repeating section', function () {

    beforeEach('Add a person', function () {
      return helpers.openQuestionnaire('test_confirmation_question_within_repeating_section.json').then(() => {
        return browser
          .click(DoesAnyoneLiveHerePage.yes())
          .click(DoesAnyoneLiveHerePage.submit())
          .setValue(AddPersonPage.firstName(), 'John')
          .setValue(AddPersonPage.lastName(), 'Doe')
          .click(AddPersonPage.submit())
          .click(DoesAnyoneLiveHerePage.no())
          .click(DoesAnyoneLiveHerePage.submit())
          .getUrl().should.eventually.contain(NumberOfEmployeesTotalPage.url().split('/').slice(-1)[0]);
      });
    });

    describe('Given a confirmation question', function () {

      it('When I answer \'No\' to the confirmation question, Then I should be routed back to the source question', function () {
        return browser
          .click(NumberOfEmployeesTotalPage.submit())
          .click(ConfirmZeroEmployeesPage.no())
          .click(ConfirmZeroEmployeesPage.submit())
          .getUrl().should.eventually.contain(NumberOfEmployeesTotalPage.pageName);
      });

    });

    describe('Given I have answered a confirmation question', function () {

      it('When I view the summary, Then the confirmation question should not be displayed', function () {
        return browser
          .setValue(NumberOfEmployeesTotalPage.numberOfEmployeesTotal(), 0)
          .click(NumberOfEmployeesTotalPage.submit())
          .click(ConfirmZeroEmployeesPage.yes())
          .click(ConfirmZeroEmployeesPage.submit())
          .getUrl().should.eventually.contain(SummaryPage.pageName)
          .isExisting(SummaryPage.confirmZeroEmployeesAnswer()).should.eventually.be.false;
      });

    });

    describe('Given a question with a skip condition', function () {

      it('When I submit an answer that is at least \'1\', Then I should be skipped past the confirmation question', function () {
        return browser
          .setValue(NumberOfEmployeesTotalPage.numberOfEmployeesTotal(), 3)
          .click(NumberOfEmployeesTotalPage.submit())
          .getUrl().should.eventually.contain(NumberOfEmployeesBreakdownPage.pageName)
          .getText(NumberOfEmployeesBreakdownPage.questionText()).should.eventually.contain('Of the 3 total employees');
      });

    });

  });

});
