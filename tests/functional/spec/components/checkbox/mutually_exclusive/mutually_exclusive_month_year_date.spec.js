const helpers = require('../../../../helpers');

const MonthYearDatePage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-month-year-date.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-month-year-section-summary.page');

describe('Component: Mutually Exclusive Month Year Date With Single Checkbox Override', function() {
  let browser;

  beforeEach(function() {
    helpers.openQuestionnaire('test_mutually_exclusive.json')
    .then(openBrowser => browser = openBrowser)
    .then(function() {
        browser.url('/questionnaire/mutually-exclusive-month-year-date');
    });
  });

  describe('Given the user has entered a value for the non-exclusive month year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

        // Given
        $(MonthYearDatePage.monthYearDateMonth()).setValue('3');
        $(MonthYearDatePage.monthYearDateYear()).setValue('2018');
        expect($(MonthYearDatePage.monthYearDateMonth()).getValue()).to.contain('3');
        expect($(MonthYearDatePage.monthYearDateYear()).getValue()).to.contain('2018');

        // When
        $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click();

        // Then
        expect($(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
        expect($(MonthYearDatePage.monthYearDateMonth()).getValue()).to.contain('');
        expect($(MonthYearDatePage.monthYearDateYear()).getValue()).to.contain('');

        $(MonthYearDatePage.submit()).click();

        expect($(SummaryPage.monthYearDateExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.monthYearDateExclusiveAnswer()).getText()).to.not.have.string('March 2018');
    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', function() {

        // Given
        $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click();
        expect($(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // When
        $(MonthYearDatePage.monthYearDateMonth()).setValue('3');
        $(MonthYearDatePage.monthYearDateYear()).setValue('2018');

        // Then
        expect($(MonthYearDatePage.monthYearDateMonth()).getValue()).to.contain('3');
        expect($(MonthYearDatePage.monthYearDateYear()).getValue()).to.contain('2018');

        expect($(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(MonthYearDatePage.submit()).click();

        expect($(SummaryPage.monthYearDateAnswer()).getText()).to.have.string('March 2018');
        expect($(SummaryPage.monthYearDateAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', function() {

        // Given
        expect($(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(MonthYearDatePage.monthYearDateMonth()).setValue('3');
        $(MonthYearDatePage.monthYearDateYear()).setValue('2018');

        // Then
        expect($(MonthYearDatePage.monthYearDateMonth()).getValue()).to.contain('3');
        expect($(MonthYearDatePage.monthYearDateYear()).getValue()).to.contain('2018');
        expect($(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(MonthYearDatePage.submit()).click();

        expect($(SummaryPage.monthYearDateAnswer()).getText()).to.have.string('March 2018');
        expect($(SummaryPage.monthYearDateAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive month year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

        // Given
        expect($(MonthYearDatePage.monthYearDateMonth()).getValue()).to.contain('');
        expect($(MonthYearDatePage.monthYearDateYear()).getValue()).to.contain('');

        // When
        $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click();
        expect($(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // Then
        $(MonthYearDatePage.submit()).click();

        expect($(SummaryPage.monthYearDateExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.monthYearDateExclusiveAnswer()).getText()).to.not.have.string('March 2018');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

        // Given
        expect($(MonthYearDatePage.monthYearDateMonth()).getValue()).to.contain('');
        expect($(MonthYearDatePage.monthYearDateYear()).getValue()).to.contain('');
        expect($(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(MonthYearDatePage.submit()).click();

        // Then
        expect($(SummaryPage.monthYearDateAnswer()).getText()).to.contain('No answer provided');

    });
  });

});
