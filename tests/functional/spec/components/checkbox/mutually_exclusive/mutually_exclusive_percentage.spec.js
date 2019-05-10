const helpers = require('../../../../helpers');

const PercentagePage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-percentage.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-percentage-section-summary.page');

describe('Component: Mutually Exclusive Percentage With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-percentage');
        });
  });

  describe('Given the user has entered a value for the non-exclusive percentage answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .setValue(PercentagePage.percentage(), '99')
        .getValue(PercentagePage.percentage()).should.eventually.contain('99')

        // When
        .click(PercentagePage.percentageExclusiveIPreferNotToSay())

        // Then
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(PercentagePage.percentage()).should.eventually.contain('')

        .click(PercentagePage.submit())

        .getText(SummaryPage.percentageExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.percentageExclusiveAnswer()).should.not.eventually.have.string('99');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive percentage answer and removes focus, Then only the non-exclusive percentage answer should be answered.', function() {

      return browser
        // Given
        .click(PercentagePage.percentageExclusiveIPreferNotToSay())
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .setValue(PercentagePage.percentage(), '99')

        // Then
        .getValue(PercentagePage.percentage()).should.eventually.contain('99')
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(PercentagePage.submit())

        .getText(SummaryPage.percentageAnswer()).should.eventually.have.string('99')
        .getText(SummaryPage.percentageAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive percentage answer, Then only the non-exclusive percentage answer should be answered.', function() {

      return browser
        // Given
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(PercentagePage.percentage(), '99')

        // Then
        .getValue(PercentagePage.percentage()).should.eventually.contain('99')
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(PercentagePage.submit())

        .getText(SummaryPage.percentageAnswer()).should.eventually.have.string('99')
        .getText(SummaryPage.percentageAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive percentage answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(PercentagePage.percentage()).should.eventually.contain('')

        // When
        .click(PercentagePage.percentageExclusiveIPreferNotToSay())
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(PercentagePage.submit())

        .getText(SummaryPage.percentageExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.percentageExclusiveAnswer()).should.not.eventually.have.string('British\nIrish');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(PercentagePage.percentage()).should.eventually.contain('')
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(PercentagePage.submit())

        // Then
        .getText(SummaryPage.percentageAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
