const helpers = require('../../../../helpers');

const MandatoryCheckboxPage = require('../../../../pages/components/checkbox/mutually-exclusive/mutually-exclusive-checkbox.page');
const SummaryPage = require('../../../../pages/components/checkbox/mutually-exclusive/mandatory-section-summary.page');

describe('Component: Mutually Exclusive Checkbox With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json');
  });

  describe('Given the user has clicked multiple non-exclusive options', function() {
    it('When then user clicks the mutually exclusive option, Then only the mutually exclusive option should be checked.', function() {

      return browser
        // Given
        .click(MandatoryCheckboxPage.checkboxBritish())
        .click(MandatoryCheckboxPage.checkboxIrish())
        .click(MandatoryCheckboxPage.checkboxOther())
        .setValue(MandatoryCheckboxPage.checkboxOtherText(), 'The other option')

        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.checkboxOther()).should.eventually.be.true
        .getValue(MandatoryCheckboxPage.checkboxOtherText()).should.eventually.contain('The other option')

        // When
        .click(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay())
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.checkboxOther()).should.eventually.be.false
        .getValue(MandatoryCheckboxPage.checkboxOtherText()).should.eventually.contain('')

        .click(MandatoryCheckboxPage.submit())

        .getText(SummaryPage.checkboxExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.checkboxExclusiveAnswer()).should.not.eventually.have.string('British\nIrish');

    });
  });

  describe('Given the user has clicked the mutually exclusive option', function() {
    it('When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.', function() {

      return browser
        // Given
        .click(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay())
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .click(MandatoryCheckboxPage.checkboxBritish())
        .click(MandatoryCheckboxPage.checkboxIrish())

        // Then
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should.eventually.be.true

        .click(MandatoryCheckboxPage.submit())

        .getText(SummaryPage.checkboxAnswer()).should.eventually.have.string('British\nIrish')
        .getText(SummaryPage.checkboxAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive option', function() {
    it('When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.', function() {

      return browser
        // Given
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(MandatoryCheckboxPage.checkboxBritish())
        .click(MandatoryCheckboxPage.checkboxIrish())

        // Then
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should.eventually.be.true

        .click(MandatoryCheckboxPage.submit())

        .getText(SummaryPage.checkboxAnswer()).should.eventually.have.string('British\nIrish')
        .getText(SummaryPage.checkboxAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked any of the non-exclusive options', function() {
    it('When the user clicks the mutually exclusive option, Then only the exclusive option should be checked.', function() {

      return browser
        // Given
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.checkboxOther()).should.eventually.be.false

        // When
        .click(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay())
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should.eventually.be.true
        .click(MandatoryCheckboxPage.submit())

        // Then
        .getText(SummaryPage.checkboxExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.checkboxExclusiveAnswer()).should.not.eventually.have.string('British\nIrish');

    });
  });

  describe('Given the user has not clicked any options and the question is mandatory', function() {
    it('When the user clicks the Continue button, Then a validation error message should be displayed.', function() {

      return browser
        // Given
        .isSelected(MandatoryCheckboxPage.checkboxBritish()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.checkboxIrish()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.checkboxOther()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(MandatoryCheckboxPage.submit())

        // Then
        .getText(MandatoryCheckboxPage.errorHeader()).should.eventually.contain('This page has an error')
        .getText(MandatoryCheckboxPage.errorNumber(1)).should.eventually.contain('Enter an answer to continue');

    });
  });

});
