const helpers = require('../../../../helpers');

const UnitPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-unit-section-summary.page');

describe('Component: Mutually Exclusive Unit With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-unit');
        });
  });

  describe('Given the user has entered a value for the non-exclusive unit answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .setValue(UnitPage.unit(), '10')
        .getValue(UnitPage.unit()).should.eventually.contain('10')

        // When
        .click(UnitPage.unitExclusiveIPreferNotToSay())

        // Then
        .isSelected(UnitPage.unitExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(UnitPage.unit()).should.eventually.contain('')

        .click(UnitPage.submit())

        .getText(SummaryPage.unitExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.unitExclusiveAnswer()).should.not.eventually.have.string('10');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive unit answer and removes focus, Then only the non-exclusive unit answer should be answered.', function() {

      return browser
        // Given
        .click(UnitPage.unitExclusiveIPreferNotToSay())
        .isSelected(UnitPage.unitExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .setValue(UnitPage.unit(), '10')

        // Then
        .getValue(UnitPage.unit()).should.eventually.contain('10')
        .click(UnitPage.unitLabel())
        .isSelected(UnitPage.unitExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(UnitPage.submit())

        .getText(SummaryPage.unitAnswer()).should.eventually.have.string('10')
        .getText(SummaryPage.unitAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive unit answer, Then only the non-exclusive unit answer should be answered.', function() {

      return browser
        // Given
        .isSelected(UnitPage.unitExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(UnitPage.unit(), '10')

        // Then
        .getValue(UnitPage.unit()).should.eventually.contain('10')
        .isSelected(UnitPage.unitExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(UnitPage.submit())

        .getText(SummaryPage.unitAnswer()).should.eventually.have.string('10')
        .getText(SummaryPage.unitAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive unit answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(UnitPage.unit()).should.eventually.contain('')

        // When
        .click(UnitPage.unitExclusiveIPreferNotToSay())
        .isSelected(UnitPage.unitExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(UnitPage.submit())

        .getText(SummaryPage.unitExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.unitExclusiveAnswer()).should.not.eventually.have.string('10');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(UnitPage.unit()).should.eventually.contain('')
        .isSelected(UnitPage.unitExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(UnitPage.submit())

        // Then
        .getText(SummaryPage.unitAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
