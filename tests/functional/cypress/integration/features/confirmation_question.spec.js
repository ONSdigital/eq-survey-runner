import {openQuestionnaire} from ../../helpers/helpers.js

const NumberOfEmployeesTotalBlockPage = require('../../generated_pages/confirmation_question/number-of-employees-total-block.page.js');
const ConfirmZeroEmployeesBlockPage = require('../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js');
const SummaryPage = require('../../generated_pages/confirmation_question/summary.page.js');
const ThankYouPage = require('../../base_pages/thank-you.page.js');

describe('Feature: Confirmation Question', function() {

  describe('Given I have a confirmation Question', function() {

    before('Get to summary', function () {
      openQuestionnaire('test_confirmation_question.json')
                  .get(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).type(0)
          .get(NumberOfEmployeesTotalBlockPage.submit()).click()
          .get(ConfirmZeroEmployeesBlockPage.yes()).click()
          .get(ConfirmZeroEmployeesBlockPage.submit()).click()
          .url().should('contain', SummaryPage.pageName);
      });
    });

    it('When I view the summary, Then the confirmation question should not be displayed', function () {
              .get(SummaryPage.numberOfEmployeesTotal()).stripText().should('contain', '0')
        .elements(SummaryPage.confirmZeroEmployeesAnswer()).then(result => result.value).should.eventually.be.empty;
    });

    it('When I view my responses, Then the confirmation question should not be displayed', function () {
              .get(SummaryPage.submit()).click()
        .get(ThankYouPage.viewSubmitted()).click()
        .url().should('contain', 'view-submission')
        .get(SummaryPage.numberOfEmployeesTotal()).stripText().should('contain', '0')
        .elements(SummaryPage.confirmZeroEmployeesAnswer()).then(result => result.value).should.eventually.be.empty;
    });

  });
});

