const helpers = require('../../../helpers');

const IncorrectAnswerPage = require('../../../generated_pages/routing_date_equals/incorrect-answer.page.js');
const CorrectAnswerPage =   require('../../../generated_pages/routing_date_equals/correct-answer.page.js');

describe('Feature: Routing on a Date', function () {
  describe('Equals', function () {
    let browser;

    describe('Given I start date routing equals survey', function () {
      const ComparisonDateQuestionPage = require('../../../generated_pages/routing_date_equals/comparison-date-block.page');
      const DateQuestionPage = require('../../../generated_pages/routing_date_equals/date-question.page');

      beforeEach(function() {
        helpers.openQuestionnaire('test_routing_date_equals.json').then(openBrowser => browser = openBrowser);

        $(ComparisonDateQuestionPage.day()).setValue(31);
        $(ComparisonDateQuestionPage.month()).setValue(3);
        $(ComparisonDateQuestionPage.year()).setValue(2020);
        $(ComparisonDateQuestionPage.submit()).click();
      });

      it('When I enter the same date, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(31);
        $(DateQuestionPage.month()).setValue(3);
        $(DateQuestionPage.year()).setValue(2020);
        $(DateQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the yesterday date, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(30);
        $(DateQuestionPage.month()).setValue(3);
        $(DateQuestionPage.year()).setValue(2020);
        $(DateQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the tomorrow date, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(1);
        $(DateQuestionPage.month()).setValue(4);
        $(DateQuestionPage.year()).setValue(2020);
        $(DateQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the last month date, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(29);
        $(DateQuestionPage.month()).setValue(2);
        $(DateQuestionPage.year()).setValue(2020);
        $(DateQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the next month date, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(30);
        $(DateQuestionPage.month()).setValue(4);
        $(DateQuestionPage.year()).setValue(2020);
        $(DateQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the last year date, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(31);
        $(DateQuestionPage.month()).setValue(3);
        $(DateQuestionPage.year()).setValue(2019);
        $(DateQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the next year date, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(31);
        $(DateQuestionPage.month()).setValue(3);
        $(DateQuestionPage.year()).setValue(2021);
        $(DateQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter an incorrect date, Then I should be routed to the incorrect page', function () {
        $(DateQuestionPage.day()).setValue(1);
        $(DateQuestionPage.month()).setValue(3);
        $(DateQuestionPage.year()).setValue(2020);
        $(ComparisonDateQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });
    });
  });

  describe('Not Equals', function () {
    let browser;

    describe('Given I start date routing not equals survey', function () {
      const DateQuestionPage = require('../../../generated_pages/routing_date_not_equals/date-question.page');

      beforeEach(function() {
        helpers.openQuestionnaire('test_routing_date_not_equals.json').then(openBrowser => browser = openBrowser);
      });

      it('When I enter a different date to 28/02/2018, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(27);
        $(DateQuestionPage.month()).setValue(2);
        $(DateQuestionPage.year()).setValue(2018);
        $(DateQuestionPage.submit()).click();

        let expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter 28/02/2018, Then I should be routed to the incorrect page', function () {
        $(DateQuestionPage.day()).setValue(28);
        $(DateQuestionPage.month()).setValue(2);
        $(DateQuestionPage.year()).setValue(2018);
        $(DateQuestionPage.submit()).click();

        let expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe('Greater Than', function () {
    describe('Given I start date routing greater than survey', function () {
      let browser;

      const DateQuestionPage = require('../../../generated_pages/routing_date_greater_than/date-question.page');

      beforeEach(function() {
        helpers.openQuestionnaire('test_routing_date_greater_than.json')
          .then(openBrowser => browser = openBrowser);
      });

      it('When I enter a date greater than March 2017, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.Month()).setValue(4);
        $(DateQuestionPage.Year()).setValue(2017);
        $(DateQuestionPage.submit()).click();

        let expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a date less than or equal to March 2017, Then I should be routed to the incorrect page', function () {
        $(DateQuestionPage.Month()).setValue(3);
        $(DateQuestionPage.Year()).setValue(2017);
        $(DateQuestionPage.submit()).click();

        let expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe('Less Than', function () {
    describe('Given I start date routing less than survey', function () {
      let browser;
      const DateQuestionPage = require('../../../generated_pages/routing_date_less_than/date-question.page');

      // TODAY
      let today = new Date();

      // YESTERDAY
      let yesterday = new Date(today);
      yesterday.setDate(today.getDate() - 1);

      let dd_yesterday = yesterday.getDate(); // yesterday
      let mm_yesterday = yesterday.getMonth()+1; //January is 0!
      let yyyy_yesterday = yesterday.getFullYear();

      beforeEach(function() {
        helpers.openQuestionnaire('test_routing_date_less_than.json').then(openBrowser => browser = openBrowser);
      });

      it('When I enter a date less than today, Then I should be routed to the correct page', function () {
        $(DateQuestionPage.day()).setValue(dd_yesterday);
        $(DateQuestionPage.month()).setValue(mm_yesterday);
        $(DateQuestionPage.year()).setValue(yyyy_yesterday);
        $(DateQuestionPage.submit()).click();

        let browserUrl = browser.getUrl();

        expect(browserUrl).to.contain(CorrectAnswerPage.pageName);
      });
    });
  });

});
