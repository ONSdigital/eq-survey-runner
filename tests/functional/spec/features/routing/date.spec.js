const helpers = require('../../../helpers');

const IncorrectAnswerPage = require('../../../pages/features/routing/date/incorrect-answer.page.js');
const CorrectAnswerPage = require('../../../pages/features/routing/date/correct-answer.page.js');

describe('Feature: Routing on a Date', function () {

  describe('Equals', function () {
    describe('Given I start date routing equals survey', function () {

      var ComparisonDateQuestionPage = require('../../../pages/features/routing/date/equals/comparison-date-block.page');
      var DateQuestionPage = require('../../../pages/features/routing/date/equals/date-question.page');

      beforeEach(function() {
        return helpers.openQuestionnaire('test_routing_date_equals.json').then(() => {
          return browser
            .setValue(ComparisonDateQuestionPage.day(), 31)
            .selectByValue(ComparisonDateQuestionPage.month(), 3)
            .setValue(ComparisonDateQuestionPage.year(), 2020)
            .click(ComparisonDateQuestionPage.submit())
            .getUrl().should.eventually.contain(DateQuestionPage.pageName);
        });
      });

      it('When I enter the same date, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 31)
          .selectByValue(DateQuestionPage.month(), 3)
          .setValue(DateQuestionPage.year(), 2020)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the yesterday date, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 30)
          .selectByValue(DateQuestionPage.month(), 3)
          .setValue(DateQuestionPage.year(), 2020)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the tomorrow date, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 1)
          .selectByValue(DateQuestionPage.month(), 4)
          .setValue(DateQuestionPage.year(), 2020)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the last month date, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 29)
          .selectByValue(DateQuestionPage.month(), 2)
          .setValue(DateQuestionPage.year(), 2020)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the next month date, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 30)
          .selectByValue(DateQuestionPage.month(), 4)
          .setValue(DateQuestionPage.year(), 2020)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the last year date, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 31)
          .selectByValue(DateQuestionPage.month(), 3)
          .setValue(DateQuestionPage.year(), 2019)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter the next year date, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 31)
          .selectByValue(DateQuestionPage.month(), 3)
          .setValue(DateQuestionPage.year(), 2021)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter an incorrect date, Then I should be routed to the incorrect page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 1)
          .selectByValue(DateQuestionPage.month(), 3)
          .setValue(DateQuestionPage.year(), 2020)
          .click(ComparisonDateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });
    });
  });

  describe('Not Equals', function () {
    describe('Given I start date routing not equals survey', function () {

      var DateQuestionPage = require('../../../pages/features/routing/date/not_equals/date-question.page');

      beforeEach(function() {
        return helpers.openQuestionnaire('test_routing_date_not_equals.json').then(() => {
          return browser
            .getUrl().should.eventually.contain(DateQuestionPage.pageName);
        });
      });

      it('When I enter a different date to 28/02/2018, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 27)
          .selectByValue(DateQuestionPage.month(), 2)
          .setValue(DateQuestionPage.year(), 2018)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter 28/02/2018, Then I should be routed to the incorrect page', function () {
        return browser
          .setValue(DateQuestionPage.day(), 28)
          .selectByValue(DateQuestionPage.month(), 2)
          .setValue(DateQuestionPage.year(), 2018)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });

    });
  });

  describe('Greater Than', function () {
    describe('Given I start number routing not equals survey', function () {

      var DateQuestionPage = require('../../../pages/features/routing/date/greater_than/date-question.page');

      beforeEach(function() {
        return helpers.openQuestionnaire('test_routing_date_greater_than.json').then(() => {
          return browser
            .getUrl().should.eventually.contain(DateQuestionPage.pageName);
        });
      });

      it('When I enter a date greater than March 2017, Then I should be routed to the correct page', function () {
        return browser
          .selectByValue(DateQuestionPage.month(), 4)
          .setValue(DateQuestionPage.year(), 2017)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a date less than or equal to March 2017, Then I should be routed to the incorrect page', function () {
        return browser
          .selectByValue(DateQuestionPage.month(), 3)
          .setValue(DateQuestionPage.year(), 2017)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });

    });
  });

  describe('Less Than', function () {
    describe('Given I start number routing not equals survey', function () {

      var DateQuestionPage = require('../../../pages/features/routing/date/less_than/date-question.page');
      var today = new Date();
      var dd_today = today.getDate(); // today
      var dd_yesterday = today.getDate()-1; // yesterday
      var mm = today.getMonth()+1; //January is 0!
      var yyyy = today.getFullYear();

      beforeEach(function() {
        return helpers.openQuestionnaire('test_routing_date_less_than.json').then(() => {
          return browser
            .getUrl().should.eventually.contain(DateQuestionPage.pageName);
        });
      });

      it('When I enter a date less than today, Then I should be routed to the correct page', function () {
        return browser
          .setValue(DateQuestionPage.day(), dd_yesterday)
          .selectByValue(DateQuestionPage.month(), mm)
          .setValue(DateQuestionPage.year(), yyyy)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a date greater than or equal to today, Then I should be routed to the incorrect page', function () {
        return browser
          .setValue(DateQuestionPage.day(), dd_today)
          .selectByValue(DateQuestionPage.month(), mm)
          .setValue(DateQuestionPage.year(), yyyy)
          .click(DateQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });

    });
  });

});
