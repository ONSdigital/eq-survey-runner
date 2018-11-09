const helpers = require('../../../helpers');

describe('Feature: Routing on a Number', function () {
  describe('Equals', function () {
    describe('Given I start number routing equals survey', function () {

      var NumberQuestionPage = require('../../../generated_pages/routing_number_equals/number-question.page');
      var CorrectAnswerPage = require('../../../generated_pages/routing_number_equals/correct-answer.page');
      var IncorrectAnswerPage = require('../../../generated_pages/routing_number_equals/incorrect-answer.page');

      before(function () {
        return helpers.openQuestionnaire('test_routing_number_equals.json');
      });

      it('When I enter the correct number, Then I should be routed to the correct page', function () {
        return browser
          .setValue(NumberQuestionPage.answer(), 123)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter an incorrect number, Then I should be routed to the incorrect page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 555)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe('Not Equals', function () {
    describe('Given I start number routing not equals survey', function () {

      var NumberQuestionPage = require('../../../generated_pages/routing_number_not_equals/number-question.page');
      var CorrectAnswerPage = require('../../../generated_pages/routing_number_not_equals/correct-answer.page');
      var IncorrectAnswerPage = require('../../../generated_pages/routing_number_not_equals/incorrect-answer.page');

      before(function () {
        return helpers.openQuestionnaire('test_routing_number_not_equals.json');
      });

      it('When I enter a different number, Then I should be routed to the correct page', function () {
        return browser
          .setValue(NumberQuestionPage.answer(), 987)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a matching number, Then I should be routed to the incorrect page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 123)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe('Greater Than', function () {
    describe('Given I start number routing greater then survey', function () {

      var NumberQuestionPage = require('../../../generated_pages/routing_number_greater_than/number-question.page');
      var CorrectAnswerPage = require('../../../generated_pages/routing_number_greater_than/correct-answer.page');
      var IncorrectAnswerPage = require('../../../generated_pages/routing_number_greater_than/incorrect-answer.page');

      before(function () {
        return helpers.openQuestionnaire('test_routing_number_greater_than.json');
      });

      it('When I enter a greater number, Then I should be routed to the correct page', function () {
        return browser
          .setValue(NumberQuestionPage.answer(), 555)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a smaller number, Then I should be routed to the incorrect page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 2)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe('Less Than', function () {
    describe('Given I start number routing less then survey', function () {

      var NumberQuestionPage = require('../../../generated_pages/routing_number_less_than/number-question.page');
      var CorrectAnswerPage = require('../../../generated_pages/routing_number_less_than/correct-answer.page');
      var IncorrectAnswerPage = require('../../../generated_pages/routing_number_less_than/incorrect-answer.page');

      before(function () {
        return helpers.openQuestionnaire('test_routing_number_less_than.json');
      });

      it('When I enter a smaller number, Then I should be routed to the correct page', function () {
        return browser
          .setValue(NumberQuestionPage.answer(), 77)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a greater number, Then I should be routed to the incorrect page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 765)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe('Greater Than or Equal', function () {
    describe('Given I start number routing greater then or equal survey', function () {

      var NumberQuestionPage = require('../../../generated_pages/routing_number_greater_than_or_equal/number-question.page');
      var CorrectAnswerPage = require('../../../generated_pages/routing_number_greater_than_or_equal/correct-answer.page');
      var IncorrectAnswerPage = require('../../../generated_pages/routing_number_greater_than_or_equal/incorrect-answer.page');

      before(function () {
        return helpers.openQuestionnaire('test_routing_number_greater_than_or_equal.json');
      });

      it('When I enter a greater number, Then I should be routed to the correct page', function () {
        return browser
          .setValue(NumberQuestionPage.answer(), 555)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter an equal number, Then I should be routed to the correct page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 123)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a smaller number, Then I should be routed to the incorrect page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 2)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });
    });

    describe('Given I have number routing with a greater than or equal to single condition', function () {

      var NumberQuestionPage = require('../../../generated_pages/routing_number_greater_than_or_equal/number-question.page');
      var CorrectAnswerPage = require('../../../generated_pages/routing_number_greater_than_or_equal/correct-answer.page');
      var IncorrectAnswerPage = require('../../../generated_pages/routing_number_greater_than_or_equal/incorrect-answer.page');

      before(function () {
        return helpers.openQuestionnaire('test_routing_number_greater_than_or_equal_single_condition.json');
      });

      it('When I enter a number larger than 123, Then I should be routed to the correct page', function () {
        return browser
          .setValue(NumberQuestionPage.answer(), 555)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a number equal to 123, Then I should be routed to the correct page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 123)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a number smaller than 123, Then I should be routed to the incorrect page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 2)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe('Less Than or Equal', function () {
    describe('Given I start number routing less then or equal survey', function () {

      var NumberQuestionPage = require('../../../generated_pages/routing_number_less_than_or_equal/number-question.page');
      var CorrectAnswerPage = require('../../../generated_pages/routing_number_less_than_or_equal/correct-answer.page');
      var IncorrectAnswerPage = require('../../../generated_pages/routing_number_less_than_or_equal/incorrect-answer.page');

      before(function () {
        return helpers.openQuestionnaire('test_routing_number_less_than_or_equal.json');
      });

      it('When I enter a less number, Then I should be routed to the correct page', function () {
        return browser
          .setValue(NumberQuestionPage.answer(), 23)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter an equal number, Then I should be routed to the correct page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 123)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a greater number, Then I should be routed to the incorrect page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 546)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });
    });

    describe('Given I have number routing with a less than or equal to single condition', function () {

      var NumberQuestionPage = require('../../../generated_pages/routing_number_less_than_or_equal/number-question.page');
      var CorrectAnswerPage = require('../../../generated_pages/routing_number_less_than_or_equal/correct-answer.page');
      var IncorrectAnswerPage = require('../../../generated_pages/routing_number_less_than_or_equal/incorrect-answer.page');

      before(function () {
        return helpers.openQuestionnaire('test_routing_number_less_than_or_equal_single_condition.json');
      });

      it('When I enter a number less than 123, Then I should be routed to the correct page', function () {
        return browser
          .setValue(NumberQuestionPage.answer(), 23)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a number equal to 123, Then I should be routed to the correct page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 123)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(CorrectAnswerPage.pageName);
      });

      it('When I enter a number larger than 123, Then I should be routed to the incorrect page', function () {
        return browser
          .click(CorrectAnswerPage.previous())
          .setValue(NumberQuestionPage.answer(), 546)
          .click(NumberQuestionPage.submit())
          .getUrl().should.eventually.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

});
