const NumberOfEmployeesTotalBlockPage = require('../../generated_pages/confirmation_question/number-of-employees-total-block.page.js');
const ConfirmZeroEmployeesBlockPage = require('../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js');
const SummaryPage = require('../../generated_pages/confirmation_question/summary.page.js');

describe('Feature: Confirmation Question', function() {
  describe('Given I have a completed the confirmation question', function() {

    before('Get to summary', function () {
      browser.openQuestionnaire('test_confirmation_question.json');
    });

    it('When I view the summary, Then the confirmation question should not be displayed', function () {
      $(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).setValue(0);
      $(NumberOfEmployeesTotalBlockPage.submit()).click();
      $(ConfirmZeroEmployeesBlockPage.yes()).click();
      $(ConfirmZeroEmployeesBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
      expect($(SummaryPage.numberOfEmployeesTotal()).getText()).to.contain('0');
      expect($$(SummaryPage.confirmZeroEmployeesAnswer())).to.be.empty;
    });
  });

  describe('Given a confirmation Question', function() {

    it('When I answer \'No\' to the confirmation question, Then I should be routed back to the source question', function () {
      browser.openQuestionnaire('test_confirmation_question.json');
      $(NumberOfEmployeesTotalBlockPage.submit()).click();
      $(ConfirmZeroEmployeesBlockPage.no()).click();
      $(ConfirmZeroEmployeesBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(NumberOfEmployeesTotalBlockPage.pageName);
    });

  });

});
