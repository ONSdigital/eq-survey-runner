import {openQuestionnaire} from '../../../helpers/helpers.js';

const IncorrectAnswerPage = require('../../../../generated_pages/routing_date_equals/incorrect-answer.page.js');
const CorrectAnswerPage =   require('../../../../generated_pages/routing_date_equals/correct-answer.page.js');

describe('Feature: Routing on a Date', function() {

  describe('Equals', function() {
    describe('Given I start date routing equals survey', function() {

      var ComparisonDateQuestionPage = require('../../../../generated_pages/routing_date_equals/comparison-date-block.page');
      var DateQuestionPage = require('../../../../generated_pages/routing_date_equals/date-question.page');

      beforeEach(function() {
        openQuestionnaire('test_routing_date_equals.json')
          .get(ComparisonDateQuestionPage.day()).type(31)
          .get(ComparisonDateQuestionPage.month()).select('3')
          .get(ComparisonDateQuestionPage.year()).type(2020)
          .get(ComparisonDateQuestionPage.submit()).click()
          .url().should('contain', DateQuestionPage.pageName);
      });

      it('When I enter the same date, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(31)
          .get(DateQuestionPage.month()).select('3')
          .get(DateQuestionPage.year()).type(2020)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter the yesterday date, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(30)
          .get(DateQuestionPage.month()).select('3')
          .get(DateQuestionPage.year()).type(2020)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter the tomorrow date, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(1)
          .get(DateQuestionPage.month()).select('4')
          .get(DateQuestionPage.year()).type(2020)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter the last month date, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(29)
          .get(DateQuestionPage.month()).select('2')
          .get(DateQuestionPage.year()).type(2020)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter the next month date, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(30)
          .get(DateQuestionPage.month()).select('4')
          .get(DateQuestionPage.year()).type(2020)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter the last year date, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(31)
          .get(DateQuestionPage.month()).select('3')
          .get(DateQuestionPage.year()).type(2019)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter the next year date, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(31)
          .get(DateQuestionPage.month()).select('3')
          .get(DateQuestionPage.year()).type(2021)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter an incorrect date, Then I should be routed to the incorrect page', function() {
        cy
          .get(DateQuestionPage.day()).type(1)
          .get(DateQuestionPage.month()).select('3')
          .get(DateQuestionPage.year()).type(2020)
          .get(ComparisonDateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });
    });
  });

  describe('Not Equals', function() {
    describe('Given I start date routing not equals survey', function() {

      var DateQuestionPage = require('../../../../generated_pages/routing_date_not_equals/date-question.page');

      beforeEach(function() {
        openQuestionnaire('test_routing_date_not_equals.json')
          .url().should('contain', DateQuestionPage.pageName);
      });

      it('When I enter a different date to 28/02/2018, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(27)
          .get(DateQuestionPage.month()).select('2')
          .get(DateQuestionPage.year()).type(2018)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter 28/02/2018, Then I should be routed to the incorrect page', function() {
        cy
          .get(DateQuestionPage.day()).type(28)
          .get(DateQuestionPage.month()).select('2')
          .get(DateQuestionPage.year()).type(2018)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', IncorrectAnswerPage.pageName);
      });

    });
  });

  describe('Greater Than', function() {
    describe('Given I start date routing greater than survey', function() {

      var DateQuestionPage = require('../../../../generated_pages/routing_date_greater_than/date-question.page');

      beforeEach(function() {
        openQuestionnaire('test_routing_date_greater_than.json')
          .url().should('contain', DateQuestionPage.pageName);
      });

      it('When I enter a date greater than March 2017, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.Month()).select('4')
          .get(DateQuestionPage.Year()).type(2017)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter a date less than or equal to March 2017, Then I should be routed to the incorrect page', function() {
        cy
          .get(DateQuestionPage.Month()).select('3')
          .get(DateQuestionPage.Year()).type(2017)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', IncorrectAnswerPage.pageName);
      });

    });
  });

  describe('Less Than', function() {
    describe('Given I start date routing less than survey', function() {

      var DateQuestionPage = require('../../../../generated_pages/routing_date_less_than/date-question.page');
      // TODAY
      var today = new Date();
      var dd_today = today.getDate();
      var mm_today = String(today.getMonth()+1);
      var yyyy_today = today.getFullYear();

      // YESTERDAY
      var yesterday = new Date(today);
      yesterday.setDate(today.getDate() - 1);
      var dd_yesterday = yesterday.getDate(); // yesterday
      var mm_yesterday = String(yesterday.getMonth()+1); //January is 0!
      var yyyy_yesterday = yesterday.getFullYear();

      const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ];

      beforeEach(function() {
        openQuestionnaire('test_routing_date_less_than.json')
          .url().should('contain', DateQuestionPage.pageName);
      });

      it('When I enter a date less than today, Then I should be routed to the correct page', function() {
        cy
          .get(DateQuestionPage.day()).type(dd_yesterday)
          .get(DateQuestionPage.month()).select(mm_yesterday)
          .get(DateQuestionPage.year()).type(yyyy_yesterday)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', CorrectAnswerPage.pageName);
      });

      it('When I enter a date greater than or equal to today, Then I should be routed to the incorrect page', function() {
        cy
          .get(DateQuestionPage.questionText()).stripText().should('contain', 'Enter a date less than ' + dd_today + ' ' + monthNames[today.getMonth()] + ' ' + yyyy_today)
          .get(CorrectAnswerPage.questionText()).stripText().should('contain', '')
          .get(DateQuestionPage.day()).type(dd_today)
          .get(DateQuestionPage.month()).select(mm_today)
          .get(DateQuestionPage.year()).type(yyyy_today)
          .get(DateQuestionPage.submit()).click()
          .url().should('contain', IncorrectAnswerPage.pageName);
      });

    });
  });

});
