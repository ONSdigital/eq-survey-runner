const helpers = require('../../../../helpers');

const MandatoryCheckboxPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-checkbox.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/mandatory-section-summary.page');

describe('Component: Mutually Exclusive Checkbox With Single Checkbox Override', function() {
  beforeEach(function() {
    helpers.openQuestionnaire('test_mutually_exclusive.json');
  });

  describe('Given the user has clicked multiple non-exclusive options', function() {
    it('When then user clicks the mutually exclusive option, Then only the mutually exclusive option should be checked.', function() {
      // Given
      $(MandatoryCheckboxPage.checkboxBritish()).click();
      $(MandatoryCheckboxPage.checkboxIrish()).click();
      $(MandatoryCheckboxPage.checkboxOther()).click();
      $(MandatoryCheckboxPage.checkboxOtherDetail()).setValue('The other option');

      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain('The other option');

      // When
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain('');

      $(MandatoryCheckboxPage.submit()).click();

      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string('British\nIrish');

    });
  });

  describe('Given the user has clicked the mutually exclusive "other" option', function() {
    it('When the user returns to the question, Then the mutually exclusive other option should remain checked.', function() {
      // Given
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      $(MandatoryCheckboxPage.submit()).click();

      // When
      $(SummaryPage.previous()).click();

      // Then
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
    });
  });

  describe('Given the user has clicked the mutually exclusive option', function() {
    it('When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.', function() {
      // Given
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      $(MandatoryCheckboxPage.checkboxBritish()).click();
      $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      $(MandatoryCheckboxPage.submit()).click();

      expect($(SummaryPage.checkboxAnswer()).getText()).to.have.string('British\nIrish');
      expect($(SummaryPage.checkboxAnswer()).getText()).to.not.have.string('I prefer not to say');
    });
  });

  describe('Given the user has not clicked the mutually exclusive option', function() {
    it('When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.', function() {
      // Given
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(MandatoryCheckboxPage.checkboxBritish()).click();
      $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      $(MandatoryCheckboxPage.submit()).click();

      expect($(SummaryPage.checkboxAnswer()).getText()).to.have.string('British\nIrish');
      expect($(SummaryPage.checkboxAnswer()).getText()).to.not.have.string('I prefer not to say');
    });
  });

  describe('Given the user has not clicked any of the non-exclusive options', function() {
    it('When the user clicks the mutually exclusive option, Then only the exclusive option should be checked.', function() {
      // Given
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;

      // When
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      $(MandatoryCheckboxPage.submit()).click();

      // Then
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string('British\nIrish');
    });
  });

  describe('Given the user has not clicked any options and the question is mandatory', function() {
    it('When the user clicks the Continue button, Then a validation error message should be displayed.', function() {
      // Given
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(MandatoryCheckboxPage.submit()).click();

      // Then
      expect($(MandatoryCheckboxPage.errorHeader()).getText()).to.contain('This page has an error');
      expect($(MandatoryCheckboxPage.errorNumber(1)).getText()).to.contain('Enter an answer to continue');
    });
  });

});
