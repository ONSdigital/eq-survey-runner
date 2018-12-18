import {openQuestionnaire} from ../../helpers/helpers.js

const RadioPage = require('../../generated_pages/view_submitted_response/radio.page.js');
const NumberBlockPage = require('../../generated_pages/view_submitted_response/test-number-block.page.js');
const SummaryPage = require('../../generated_pages/view_submitted_response/summary.page.js');
const BaseSummaryPage = require('../../base_pages/summary.page.js');
const ThankYouPage = require('../../base_pages/thank-you.page.js');


describe('Feature: Submitted Responses', function() {

  beforeEach(function() {
    openQuestionnaire('test_view_submitted_response.json')
                  .get(RadioPage.bacon()).click()
          .get(RadioPage.submit()).click()
          .get(NumberBlockPage.testCurrency()).type(123.45)
          .get(NumberBlockPage.submit()).click();
    });
  });

  describe('Check submitted responses', function() {
    it('Given I complete to Thank-You page, When I click the submitted answers link, Then I should be able to view my submitted answers', function() {
                  .get(BaseSummaryPage.viewSubmissionText()).stripText().should('contain', 'opportunity to view and print a copy of your answers')
          .get(SummaryPage.submit()).click()
          .get(ThankYouPage.viewSubmitted()).click()
          .url().should('contain', 'view-submission')
          .get(SummaryPage.radioAnswer()).stripText().should('contain', 'Bacon')
          .get(SummaryPage.testCurrency()).stripText().should('contain', '123.45');
    });

    it('Given I am viewing my submitted answers, When I click refresh after the timeout period, Then I should be routed back to Thank You page', function() {
                  .get(SummaryPage.submit()).click()
          .waitUntil(function () {
                          .refresh()
              .isVisible(ThankYouPage.viewSubmissionExpired());
          }, 6000, 'Can still view submission after timeout');
    });
  });

  describe('Try to click view submission link after timeout', function() {
    it('Given I complete to Thank-You page, When I click the submitted answers link after the timeout period, Then I should not be able to view my submitted answers', function() {
                  .get(SummaryPage.submit()).click()
          .isVisible(ThankYouPage.viewSubmitted())
          .pause(5000)
          .get(ThankYouPage.viewSubmitted()).click()
          .isVisible(ThankYouPage.viewSubmissionExpired());
    });
  });

  describe('Check view submission link has expired after timeout', function() {
    it('Given I complete to Thank-You page, When I refresh after the timeout period, Then I should not be able to view my submitted answers', function() {
                  .get(SummaryPage.submit()).click()
          .isVisible(ThankYouPage.viewSubmitted())
          .waitUntil(function () {
                          .refresh()
              .isVisible(ThankYouPage.viewSubmissionExpired());
          }, 6000, 'Can still view submission after timeout');
    });
  });

});

