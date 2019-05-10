const helpers = require('../../../../helpers');

const YearDatePage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-year-date.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-year-section-summary.page');

describe('Component: Mutually Exclusive Year Date With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-year-date');
        });
  });

  describe('Given the user has entered a value for the non-exclusive year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .setValue(YearDatePage.yearDateYear(), '2018')
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('2018')

        // When
        .click(YearDatePage.yearDateExclusiveIPreferNotToSay())

        // Then
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('')

        .click(YearDatePage.submit())

        .getText(SummaryPage.yearDateExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.yearDateExclusiveAnswer()).should.not.eventually.have.string('2018');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive year date answer and removes focus, Then only the non-exclusive year date answer should be answered.', function() {

      return browser
        // Given
        .click(YearDatePage.yearDateExclusiveIPreferNotToSay())
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .setValue(YearDatePage.yearDateYear(), '2018')

        // Then
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('2018')
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(YearDatePage.submit())

        .getText(SummaryPage.yearDateAnswer()).should.eventually.have.string('2018')
        .getText(SummaryPage.yearDateAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive year date answer, Then only the non-exclusive year date answer should be answered.', function() {

      return browser
        // Given
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(YearDatePage.yearDateYear(), '2018')

        // Then
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('2018')
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(YearDatePage.submit())

        .getText(SummaryPage.yearDateAnswer()).should.eventually.have.string('2018')
        .getText(SummaryPage.yearDateAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('')

        // When
        .click(YearDatePage.yearDateExclusiveIPreferNotToSay())
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(YearDatePage.submit())

        .getText(SummaryPage.yearDateExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.yearDateExclusiveAnswer()).should.not.eventually.have.string('2018');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('')
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(YearDatePage.submit())

        // Then
        .getText(SummaryPage.yearDateAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
