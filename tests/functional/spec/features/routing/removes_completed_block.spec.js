const helpers = require('../../../helpers');

const NumberOfEmployeesTotalBlockPage = require('../../../pages/features/confirmation_question/number-of-employees-total-block.page.js');
const ConfirmZeroEmployeesBlockPage = require('../../../pages/features/confirmation_question/confirm-zero-employees-block.page.js');
const SummaryPage = require('../../../pages/features/confirmation_question/summary.page.js');

describe('Feature: Routing incompletes block if routing backwards', function() {

  describe('Given I have a confirmation Question', function() {

    before('Get to summary', function () {
      return helpers.openQuestionnaire('test_confirmation_question.json').then(() => {
        return browser
          .setValue(NumberOfEmployeesTotalBlockPage.answer(), 0)
          .click(NumberOfEmployeesTotalBlockPage.submit())
          .click(ConfirmZeroEmployeesBlockPage.yes())
          .click(ConfirmZeroEmployeesBlockPage.submit())
          .getUrl().should.eventually.contain(SummaryPage.pageName);
      });
    });

    it('When I use browser back button and change confirmation to no then Summary should not be available', function () {
      return browser
        .back()
        .isVisible(helpers.navigationLink('Summary')).should.eventually.be.true
        .click(ConfirmZeroEmployeesBlockPage.no())
        .click(ConfirmZeroEmployeesBlockPage.submit())
        .isVisible(helpers.navigationLink('Summary')).should.eventually.be.false;
    });

  });
});
