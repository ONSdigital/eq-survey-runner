const helpers = require('../../helpers');

const NumberOfEmployeesTotalBlockPage = require('../../generated_pages/confirmation_question/number-of-employees-total-block.page.js');
const ConfirmZeroEmployeesBlockPage = require('../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js');
const SummaryPage = require('../../generated_pages/confirmation_question/summary.page.js');
const ThankYouPage = require('../../base_pages/thank-you.page.js');

describe('Feature: Confirmation Question', function() {

  describe('Given I have a confirmation Question', function() {

    before('Get to summary', function () {
      return helpers.openQuestionnaire('test_confirmation_question.json').then(() => {
        return browser
          .setValue(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal(), 0)
          .click(NumberOfEmployeesTotalBlockPage.submit())
          .click(ConfirmZeroEmployeesBlockPage.yes())
          .click(ConfirmZeroEmployeesBlockPage.submit())
          .getUrl().should.eventually.contain(SummaryPage.pageName);
      });
    });

    it('When I view the summary, Then the confirmation question should not be displayed', function () {
      return browser
        .getText(SummaryPage.numberOfEmployeesTotal()).should.eventually.contain('0')
        .elements(SummaryPage.confirmZeroEmployeesAnswer()).then(result => result.value).should.eventually.be.empty;
    });

    it('When I view my responses, Then the confirmation question should not be displayed', function () {
      return browser
        .click(SummaryPage.submit())
        .click(ThankYouPage.viewSubmitted())
        .getUrl().should.eventually.contain('view-submission')
        .getText(SummaryPage.numberOfEmployeesTotal()).should.eventually.contain('0')
        .elements(SummaryPage.confirmZeroEmployeesAnswer()).then(result => result.value).should.eventually.be.empty;
    });

  });
});

