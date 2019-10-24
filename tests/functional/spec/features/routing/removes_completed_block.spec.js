const helpers = require('../../../helpers');

const NumberOfEmployeesTotalBlockPage = require('../../../generated_pages/confirmation_question/number-of-employees-total-block.page.js');
const ConfirmZeroEmployeesBlockPage = require('../../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js');
const SummaryPage = require('../../../generated_pages/confirmation_question/summary.page.js');

describe('Feature: Routing incompletes block if routing backwards', function() {
  let browser;

  describe('Given I have a confirmation Question', function() {

    before('Get to summary', function () {
      helpers.openQuestionnaire('test_confirmation_question.json').then(openBrowser => browser = openBrowser);
      $(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).setValue(0);
      $(NumberOfEmployeesTotalBlockPage.submit()).click();
      $(ConfirmZeroEmployeesBlockPage.yes()).click();
      $(ConfirmZeroEmployeesBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    });

  });
});
