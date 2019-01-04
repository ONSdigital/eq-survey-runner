import {openQuestionnaire} from '../../../../helpers/helpers.js';

const MandatoryCheckboxPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-checkbox.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/mandatory-section-summary.page');

describe('Component: Mutually Exclusive Checkbox With Single Checkbox Override', function() {

  beforeEach(function() {
    return openQuestionnaire('test_mutually_exclusive.json');
  });

  describe('Given the user has clicked multiple non-exclusive options', function() {
    it('When then user clicks the mutually exclusive option, Then only the mutually exclusive option should be checked.', function() {
      cy
        // Given
        .get(MandatoryCheckboxPage.checkboxBritish()).click()
        .get(MandatoryCheckboxPage.checkboxIrish()).click()
        .get(MandatoryCheckboxPage.checkboxOther()).click()
        .get(MandatoryCheckboxPage.checkboxOtherDetail()).type('The other option')

        .get(MandatoryCheckboxPage.checkboxBritish()).should('be.checked')
        .get(MandatoryCheckboxPage.checkboxIrish()).should('be.checked')
        .get(MandatoryCheckboxPage.checkboxOther()).should('be.checked')
        .get(MandatoryCheckboxPage.checkboxOtherDetail()).invoke('val').should('contain', 'The other option')

        // When
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click()
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(MandatoryCheckboxPage.checkboxBritish()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxIrish()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxOther()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxOtherDetail()).invoke('val').should('contain', '')

        .get(MandatoryCheckboxPage.submit()).click()

        .get(SummaryPage.checkboxExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.checkboxExclusiveAnswer()).stripText().should('not.match', /British\s*Irish/);

    });
  });

  describe('Given the user has clicked the mutually exclusive option', function() {
    it('When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.', function() {
      cy
        // Given
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click()
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.checked')

        // When
        .get(MandatoryCheckboxPage.checkboxBritish()).click()
        .get(MandatoryCheckboxPage.checkboxIrish()).click()

        // Then
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxBritish()).should('be.checked')
        .get(MandatoryCheckboxPage.checkboxIrish()).should('be.checked')
        .get(MandatoryCheckboxPage.submit()).click()
        .get(SummaryPage.checkboxAnswer()).stripText().should('match', /British\s*Irish/)
        .get(SummaryPage.checkboxAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive option', function() {
    it('When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.', function() {
      cy
        // Given
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(MandatoryCheckboxPage.checkboxBritish()).click()
        .get(MandatoryCheckboxPage.checkboxIrish()).click()

        // Then
        .get(MandatoryCheckboxPage.checkboxBritish()).should('be.checked')
        .get(MandatoryCheckboxPage.checkboxIrish()).should('be.checked')

        .get(MandatoryCheckboxPage.submit()).click()

        .get(SummaryPage.checkboxAnswer()).stripText().should('match', /British\s*Irish/)
        .get(SummaryPage.checkboxAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked any of the non-exclusive options', function() {
    it('When the user clicks the mutually exclusive option, Then only the exclusive option should be checked.', function() {
      cy
        // Given
        .get(MandatoryCheckboxPage.checkboxBritish()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxIrish()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxOther()).should('not.be.checked')

        // When
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click()
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('be.checked')
        .get(MandatoryCheckboxPage.submit()).click()

        // Then
        .get(SummaryPage.checkboxExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.checkboxExclusiveAnswer()).stripText().should('not.match', /British\s*Irish/);

    });
  });

  describe('Given the user has not clicked any options and the question is mandatory', function() {
    it('When the user clicks the Continue button, Then a validation error message should be displayed.', function() {
      cy
        // Given
        .get(MandatoryCheckboxPage.checkboxBritish()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxIrish()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxOther()).should('not.be.checked')
        .get(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(MandatoryCheckboxPage.submit()).click()

        // Then
        .get(MandatoryCheckboxPage.errorHeader()).stripText().should('contain', 'This page has an error')
        .get(MandatoryCheckboxPage.errorNumber(1)).stripText().should('contain', 'Enter an answer to continue');

    });
  });

});
