const helpers = require('../../../helpers');

describe('Feature: Use of conditional Titles in Repeating blocks with condition dependant on non repeating answer', function() {
  var FavouriteColourPage = require('../../../pages/features/conditional_question_title/repeating_dependant_on_non_repeating/favourite-colour.page');
  var HouseholdCompositionPage = require('../../../pages/features/conditional_question_title/repeating_dependant_on_non_repeating/household-composition.page');
  var RepeatingBlockPage = require('../../../pages/features/conditional_question_title/repeating_dependant_on_non_repeating/repeating-block-3.page');
  var SummaryPage = require('../../../pages/features/conditional_question_title/repeating_dependant_on_non_repeating/summary.page');

  beforeEach(function() {
      return helpers.openQuestionnaire('test_titles_repeating_non_repeating_dependency.json');
  });

  describe('Given I select a favourite colour and list of names', function() {
    it('when I see each person the question title is dependant on the initial colour selected', function() {
      return browser
        .click(FavouriteColourPage.blue())
        .click(FavouriteColourPage.submit())
        .setValue(HouseholdCompositionPage.answer(),'Peter')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_1'),'Paul')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_2'),'Mary')
        .click(HouseholdCompositionPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Peter's favourite colour is Blue")
        .click(RepeatingBlockPage.yes())
        .click(RepeatingBlockPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Paul's favourite colour is Blue")
        .click(RepeatingBlockPage.yes())
        .click(RepeatingBlockPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Mary's favourite colour is Blue")
        .click(RepeatingBlockPage.yes())
        .click(RepeatingBlockPage.submit());
    });
  });

  describe('Given I select a favourite colour and list of names and get to confirm page', function() {
    it('changing the independant variable means I have to reenter values for all people', function() {
      return browser
        .click(FavouriteColourPage.blue())
        .click(FavouriteColourPage.submit())
        .setValue(HouseholdCompositionPage.answer(),'Peter')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_1'),'Paul')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_2'),'Mary')
        .click(HouseholdCompositionPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Peter's favourite colour is Blue")
        .click(RepeatingBlockPage.yes())
        .click(RepeatingBlockPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Paul's favourite colour is Blue")
        .click(RepeatingBlockPage.yes())
        .click(RepeatingBlockPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Mary's favourite colour is Blue")
        .click(RepeatingBlockPage.yes())
        .click(RepeatingBlockPage.submit())
        .click(SummaryPage.favColourAnswerEdit())
        .click(FavouriteColourPage.yellow())
        .click(FavouriteColourPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Peter's favourite colour is NOT Blue")
        .click(RepeatingBlockPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Paul's favourite colour is NOT Blue")
        .click(RepeatingBlockPage.submit())
        .getText(RepeatingBlockPage.questionText()).should.eventually.contain("Mary's favourite colour is NOT Blue");
    });
  });



});
