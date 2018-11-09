const helpers = require('../../helpers');

const RadioPage = require('../../generated_pages/view_submitted_response/radio.page.js');
const NumberBlockPage = require('../../generated_pages/view_submitted_response/test-number-block.page.js');
const SummaryPage = require('../../generated_pages/view_submitted_response/summary.page.js');
const BaseSummaryPage = require('../../base_pages/summary.page.js');
const ThankYouPage = require('../../base_pages/thank-you.page.js');


describe('Feature: Submitted Responses', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_view_submitted_response.json').then(() => {
        return browser
          .click(RadioPage.bacon())
          .click(RadioPage.submit())
          .setValue(NumberBlockPage.testCurrency(), 123.45)
          .click(NumberBlockPage.submit());
    });
  });

  describe('Check submitted responses', function() {
    it('Given I complete to Thank-You page, When I click the submitted answers link, Then I should be able to view my submitted answers', function() {
        return browser
          .getText(BaseSummaryPage.viewSubmissionText()).should.eventually.contain('opportunity to view and print a copy of your answers')
          .click(SummaryPage.submit())
          .click(ThankYouPage.viewSubmitted())
          .getUrl().should.eventually.contain('view-submission')
          .getText(SummaryPage.radioAnswer()).should.eventually.contain('Bacon')
          .getText(SummaryPage.testCurrency()).should.eventually.contain('123.45');
    });

    it('Given I am viewing my submitted answers, When I click refresh after the timeout period, Then I should be routed back to Thank You page', function() {
        return browser
          .click(SummaryPage.submit())
          .waitUntil(function () {
            return browser
              .refresh()
              .isVisible(ThankYouPage.viewSubmissionExpired());
          }, 6000, 'Can still view submission after timeout');
    });
  });

  describe('Try to click view submission link after timeout', function() {
    it('Given I complete to Thank-You page, When I click the submitted answers link after the timeout period, Then I should not be able to view my submitted answers', function() {
        return browser
          .click(SummaryPage.submit())
          .isVisible(ThankYouPage.viewSubmitted())
          .pause(5000)
          .click(ThankYouPage.viewSubmitted())
          .isVisible(ThankYouPage.viewSubmissionExpired());
    });
  });

  describe('Check view submission link has expired after timeout', function() {
    it('Given I complete to Thank-You page, When I refresh after the timeout period, Then I should not be able to view my submitted answers', function() {
        return browser
          .click(SummaryPage.submit())
          .isVisible(ThankYouPage.viewSubmitted())
          .waitUntil(function () {
            return browser
              .refresh()
              .isVisible(ThankYouPage.viewSubmissionExpired());
          }, 6000, 'Can still view submission after timeout');
    });
  });

});

