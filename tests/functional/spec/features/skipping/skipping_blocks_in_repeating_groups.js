const helpers = require('../../../helpers');


describe('Feature: Skipping in block in repeating group based on repeating answer', function() {
  var AdditionalQuestionPage = require('../../../pages/features/skipping/additional-question-block.page');
  var DobPage = require('../../../pages/features/skipping/date-of-birth.page');
  var HouseholdCompositionPage = require('../../../pages/features/skipping/household-composition.page');
  var ConfirmationPage = require('../../../pages/features/skipping/confirmation.page');

  beforeEach(function() {
      return helpers.openQuestionnaire('test_skip_conditions_on_blocks_repeating_group.json');
  });

  describe('Given I enter 3 people and give the date of birth (dob) of the first person only', function() {
    it('I should only be asked supplemental question for the one with the dob', function () {
      return browser
        .setValue(HouseholdCompositionPage.answer(), 'aaa')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_1'),'bbb')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_2'),'ccc')
        .click(HouseholdCompositionPage.submit())
        .setValue(DobPage.day(), 15)
        .setValue(DobPage.year(), '1962')
        .selectByValue(DobPage.month(), 2)
        .click(DobPage.submit())
        .click(DobPage.submit())
        .click(DobPage.submit())
        .getText(AdditionalQuestionPage.questionText()).should.eventually.contain('Some question for aaa')
        .setValue(AdditionalQuestionPage.answer(), 'random answer')
        .click(AdditionalQuestionPage.submit())
        .getText(ConfirmationPage.questionText()).should.eventually.contain('Thank you, please submit your answers.');

    });
  });

  describe('Given I enter 3 people and give the date of birth (dob) of the last person only', function() {
    it('I should only be asked supplemental question for the one with the dob', function () {
      return browser
        .setValue(HouseholdCompositionPage.answer(), 'aaa')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_1'),'bbb')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_2'),'ccc')
        .click(HouseholdCompositionPage.submit())
        .click(DobPage.submit())
        .click(DobPage.submit())
        .setValue(DobPage.day(), 15)
        .setValue(DobPage.year(), '1962')
        .selectByValue(DobPage.month(), 2)
        .click(DobPage.submit())
        .getText(AdditionalQuestionPage.questionText()).should.eventually.contain('Some question for ccc');
    });
  });
});

