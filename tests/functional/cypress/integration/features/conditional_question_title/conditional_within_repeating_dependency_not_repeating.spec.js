import {openQuestionnaire} from '../../../../helpers/helpers.js'
const FavouriteColourPage = require('../../../../generated_pages/titles_repeating_non_repeating_dependency/favourite-colour.page');
const HouseholdCompositionPage = require('../../../../generated_pages/titles_repeating_non_repeating_dependency/household-composition.page');
const RepeatingBlockPage = require('../../../../generated_pages/titles_repeating_non_repeating_dependency/repeating-block-3.page');
const SummaryPage = require('../../../../generated_pages/titles_repeating_non_repeating_dependency/summary.page');

describe('Feature: Use of conditional Titles in Repeating blocks with condition dependant on non repeating answer', function() {

  beforeEach(function() {
      return helpers.openQuestionnaire('test_titles_repeating_non_repeating_dependency.json');
  });

  describe('Given I select a favourite colour and list of names', function() {
    it('when I see each person the question title is dependant on the initial colour selected', function() {
              .get(FavouriteColourPage.blue()).click()
        .get(FavouriteColourPage.submit()).click()
        .get(HouseholdCompositionPage.firstName()).type('Peter')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_1')).type('Paul')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_2')).type('Mary')
        .get(HouseholdCompositionPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Peter's favourite colour is Blue")
        .get(RepeatingBlockPage.yes()).click()
        .get(RepeatingBlockPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Paul's favourite colour is Blue")
        .get(RepeatingBlockPage.yes()).click()
        .get(RepeatingBlockPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Mary's favourite colour is Blue")
        .get(RepeatingBlockPage.yes()).click()
        .get(RepeatingBlockPage.submit()).click();
    });
  });

  describe('Given I select a favourite colour and list of names and get to confirm page', function() {
    it('changing the independant variable means I have to reenter values for all people', function() {
              .get(FavouriteColourPage.blue()).click()
        .get(FavouriteColourPage.submit()).click()
        .get(HouseholdCompositionPage.firstName()).type('Peter')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_1')).type('Paul')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_2')).type('Mary')
        .get(HouseholdCompositionPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Peter's favourite colour is Blue")
        .get(RepeatingBlockPage.yes()).click()
        .get(RepeatingBlockPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Paul's favourite colour is Blue")
        .get(RepeatingBlockPage.yes()).click()
        .get(RepeatingBlockPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Mary's favourite colour is Blue")
        .get(RepeatingBlockPage.yes()).click()
        .get(RepeatingBlockPage.submit()).click()
        .get(SummaryPage.favColourAnswerEdit()).click()
        .get(FavouriteColourPage.yellow()).click()
        .get(FavouriteColourPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Peter's favourite colour is NOT Blue")
        .get(RepeatingBlockPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Paul's favourite colour is NOT Blue")
        .get(RepeatingBlockPage.submit()).click()
        .get(RepeatingBlockPage.questionText()).stripText().should('contain', "Mary's favourite colour is NOT Blue");
    });
  });



});
