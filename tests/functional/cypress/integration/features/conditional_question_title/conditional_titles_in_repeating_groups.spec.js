import {openQuestionnaire} from '../../../helpers/helpers.js';
const HouseholdCompositionPage = require('../../../../generated_pages/titles_within_repeating_blocks/household-composition.page');
const WhoIsAnsweringPage = require('../../../../generated_pages/titles_within_repeating_blocks/who-is-answering-block.page');
const Page1 = require('../../../../generated_pages/titles_within_repeating_blocks/repeating-block-1.page');
const Page3 = require('../../../../generated_pages/titles_within_repeating_blocks/repeating-block-3.page');

describe('Feature: Use of Titles in Repeating blocks', function() {

  beforeEach(function() {
    return openQuestionnaire('test_titles_within_repeating_blocks.json');
  });

  describe('Given I start the survey with a repeating block', function() {
    it('When I enter an  names I should see those names in the title of a subsequent questions', function() {
      cy
        .get(HouseholdCompositionPage.firstName()).type('FirstPerson')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_1')).type('SecondPerson')
        .get(HouseholdCompositionPage.submit()).click()
        .get(WhoIsAnsweringPage.questionText()).stripText().should('contain', 'Who is FirstPerson answering on behalf of?')
        .get(WhoIsAnsweringPage.chad()).click()
        .get(WhoIsAnsweringPage.submit()).click()
        .get(Page1.ageDifferenceLabel()).stripText().should('contain', 'What is their age difference to chad?')
        .get(Page1.ageDifference()).type('1')
        .get(Page1.submit()).click()
        .get(Page3.questionText()).stripText().should('contain', 'Please confirm FirstPerson’s age difference to Chad is 1')
        .get(Page3.yes()).click()
        .get(Page3.submit()).click()
        .get(WhoIsAnsweringPage.questionText()).stripText().should('contain', 'Who is SecondPerson answering on behalf of?')
        .get(WhoIsAnsweringPage.kelly()).click()
        .get(WhoIsAnsweringPage.submit()).click()
        .get(Page1.ageDifferenceLabel()).stripText().should('contain', 'What is their age difference to kelly?')
        .get(Page1.ageDifference()).type('5')
        .get(Page1.submit()).click()
        .get(Page3.questionText()).stripText().should('contain', 'Please confirm SecondPerson’s age difference to Kelly is 5')
        .get(Page3.yes()).click()
        .get(Page3.submit()).click();
    });
  });
});
