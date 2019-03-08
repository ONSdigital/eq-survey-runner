const helpers = require('../../../../helpers');

const MonthYearDatePage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-month-year-date.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-month-year-section-summary.page');

describe('Component: Mutually Exclusive Month Year Date With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-month-year-date');
        });
  });

  describe('Given the user has entered a value for the non-exclusive month year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .selectByValue(MonthYearDatePage.monthYearDateMonth(), 3)
        .setValue(MonthYearDatePage.monthYearDateYear(), '2018')
        .getText(MonthYearDatePage.monthYearDateMonth()).should.eventually.contain('March')
        .getValue(MonthYearDatePage.monthYearDateYear()).should.eventually.contain('2018')

        // When
        .click(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay())

        // Then
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(MonthYearDatePage.monthYearDateMonth()).should.eventually.contain('')
        .getValue(MonthYearDatePage.monthYearDateYear()).should.eventually.contain('')

        .click(MonthYearDatePage.submit())

        .getText(SummaryPage.monthYearDateExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.monthYearDateExclusiveAnswer()).should.not.eventually.have.string('March 2018');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', function() {

      return browser
        // Given
        .click(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay())
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .selectByValue(MonthYearDatePage.monthYearDateMonth(), 3)
        .setValue(MonthYearDatePage.monthYearDateYear(), '2018')

        // Then
        .getText(MonthYearDatePage.monthYearDateMonth()).should.eventually.contain('March')
        .getValue(MonthYearDatePage.monthYearDateYear()).should.eventually.contain('2018')

        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(MonthYearDatePage.submit())

        .getText(SummaryPage.monthYearDateAnswer()).should.eventually.have.string('March 2018')
        .getText(SummaryPage.monthYearDateAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', function() {

      return browser
        // Given
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .selectByValue(MonthYearDatePage.monthYearDateMonth(), 3)
        .setValue(MonthYearDatePage.monthYearDateYear(), '2018')

        // Then
        .getText(MonthYearDatePage.monthYearDateMonth()).should.eventually.contain('March')
        .getValue(MonthYearDatePage.monthYearDateYear()).should.eventually.contain('2018')
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(MonthYearDatePage.submit())

        .getText(SummaryPage.monthYearDateAnswer()).should.eventually.have.string('March 2018')
        .getText(SummaryPage.monthYearDateAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive month year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(MonthYearDatePage.monthYearDateMonth()).should.eventually.contain('')
        .getValue(MonthYearDatePage.monthYearDateYear()).should.eventually.contain('')

        // When
        .click(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay())
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(MonthYearDatePage.submit())

        .getText(SummaryPage.monthYearDateExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.monthYearDateExclusiveAnswer()).should.not.eventually.have.string('March 2018');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(MonthYearDatePage.monthYearDateMonth()).should.eventually.contain('')
        .getValue(MonthYearDatePage.monthYearDateYear()).should.eventually.contain('')
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(MonthYearDatePage.submit())

        // Then
        .getText(SummaryPage.monthYearDateAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
