import {openQuestionnaire} from ../../../helpers/helpers.js
const AdditionalQuestionPage = require('../../../generated_pages/skip_conditions_on_blocks_repeating_group/additional-question-block.page');
const DobPage = require('../../../generated_pages/skip_conditions_on_blocks_repeating_group/date-of-birth.page');
const HouseholdCompositionPage = require('../../../generated_pages/skip_conditions_on_blocks_repeating_group/household-composition.page');
const ConfirmationPage = require('../../../generated_pages/skip_conditions_on_blocks_repeating_group/confirmation.page');


describe('Feature: Skipping in block in repeating group based on repeating answer', function() {

  beforeEach(function() {
      return helpers.openQuestionnaire('test_skip_conditions_on_blocks_repeating_group.json');
  });

  describe('Given I enter 3 people and give the date of birth (dob) of the first person only', function() {
    it('I should only be asked supplemental question for the one with the dob', function () {
              .get(HouseholdCompositionPage.firstName()).type('aaa')
        .get(HouseholdCompositionPage.addPerson()).click()
        .clear()(HouseholdCompositionPage.firstName('_1'),'bbb')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_2')).type('ccc')
        .get(HouseholdCompositionPage.submit()).click()
        .get(DobPage.day()).type(15)
        .get(DobPage.year()).type('1962')
        .get(DobPage.month()).select(2)
        .get(DobPage.submit()).click()
        .get(DobPage.submit()).click()
        .get(DobPage.submit()).click()
        .get(AdditionalQuestionPage.questionText()).stripText().should('contain', 'Some question for aaa')
        .get(AdditionalQuestionPage.some()).type('random answer')
        .get(AdditionalQuestionPage.submit()).click()
        .get(ConfirmationPage.questionText()).stripText().should('contain', 'Thank you, please submit your answers.');

    });
  });

  describe('Given I enter 3 people and give the date of birth (dob) of the last person only', function() {
    it('I should only be asked supplemental question for the one with the dob', function () {
              .get(HouseholdCompositionPage.firstName()).type('aaa')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_1')).type('bbb')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_2')).type('ccc')
        .get(HouseholdCompositionPage.submit()).click()
        .get(DobPage.submit()).click()
        .get(DobPage.submit()).click()
        .get(DobPage.day()).type(15)
        .get(DobPage.year()).type('1962')
        .get(DobPage.month()).select(2)
        .get(DobPage.submit()).click()
        .get(AdditionalQuestionPage.questionText()).stripText().should('contain', 'Some question for ccc');
    });
  });
});

