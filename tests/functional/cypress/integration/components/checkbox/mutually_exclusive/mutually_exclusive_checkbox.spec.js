import {openQuestionnaire} from ../../../../helpers/helpers.js

const MandatoryCheckboxPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-checkbox.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/mandatory-section-summary.page');

describe('Component: Mutually Exclusive Checkbox With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json');
  });

  describe('Given the user has clicked multiple non-exclusive options', function() {
    it('When then user clicks the mutually exclusive option, Then only the mutually exclusive option should be checked.', function() {

              // Given
        .get(MandatoryCheckboxPage.checkboxBritish()).click()
        .get(MandatoryCheckboxPage.checkboxIrish()).click()
        .get(MandatoryCheckboxPage.checkboxOther()).click()
        .get(MandatoryCheckboxPage.checkboxOtherDetail()).type('The other option')

        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should('be.true')
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should('be.true')
        .isSelected(MandatoryCheckboxPage.checkboxOther()).should('be.true')
        .get(MandatoryCheckboxPage.checkboxOtherDetail()).invoke('val').should('contain', 'The other option')

        // When
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click()
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.true')

        // Then
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should('be.false')
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should('be.false')
        .isSelected(MandatoryCheckboxPage.checkboxOther()).should('be.false')
        .get(MandatoryCheckboxPage.checkboxOtherDetail()).invoke('val').should('contain', '')

        .get(MandatoryCheckboxPage.submit()).click()

        .get(SummaryPage.checkboxExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.checkboxExclusiveAnswer()).should('not.have.string', 'British\nIrish');

    });
  });

  describe('Given the user has clicked the mutually exclusive option', function() {
    it('When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.', function() {

              // Given
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click()
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.true')

        // When
        .get(MandatoryCheckboxPage.checkboxBritish()).click()
        .get(MandatoryCheckboxPage.checkboxIrish()).click()

        // Then
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.false')
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should('be.true')
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should('be.true')

        .get(MandatoryCheckboxPage.submit()).click()

        .get(SummaryPage.checkboxAnswer()).stripText().should('have.string', 'British\nIrish')
        .get(SummaryPage.checkboxAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive option', function() {
    it('When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.', function() {

              // Given
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.false')

        // When
        .get(MandatoryCheckboxPage.checkboxBritish()).click()
        .get(MandatoryCheckboxPage.checkboxIrish()).click()

        // Then
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should('be.true')
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should('be.true')

        .get(MandatoryCheckboxPage.submit()).click()

        .get(SummaryPage.checkboxAnswer()).stripText().should('have.string', 'British\nIrish')
        .get(SummaryPage.checkboxAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked any of the non-exclusive options', function() {
    it('When the user clicks the mutually exclusive option, Then only the exclusive option should be checked.', function() {

              // Given
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should('be.false')
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should('be.false')
        .isSelected(MandatoryCheckboxPage.checkboxOther()).should('be.false')

        // When
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click()
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.true')
        .get(MandatoryCheckboxPage.submit()).click()

        // Then
        .get(SummaryPage.checkboxExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.checkboxExclusiveAnswer()).should('not.have.string', 'British\nIrish');

    });
  });

  describe('Given the user has not clicked any options and the question is mandatory', function() {
    it('When the user clicks the Continue button, Then a validation error message should be displayed.', function() {

              // Given
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should('be.false')
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should('be.false')
        .isSelected(MandatoryCheckboxPage.checkboxOther()).should('be.false')
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.false')

        // When
        .get(MandatoryCheckboxPage.submit()).click()

        // Then
        .get(MandatoryCheckboxPage.errorHeader()).stripText().should('contain', 'This page has an error')
        .get(MandatoryCheckboxPage.errorNumber(1)).stripText().should('contain', 'Enter an answer to continue');

    });
  });

});
