const YearDatePage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-year-date.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-year-section-summary.page');

describe('Component: Mutually Exclusive Year Date With Single Checkbox Override', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_mutually_exclusive.json');
    browser.url('/questionnaire/mutually-exclusive-year-date');
  });

  describe('Given the user has entered a value for the non-exclusive year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      // Given
      $(YearDatePage.yearDateYear()).setValue('2018');
      expect($(YearDatePage.yearDateYear()).getValue()).to.contain('2018');

      // When
      $(YearDatePage.yearDateExclusiveIPreferNotToSay()).click();

      // Then
      expect($(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(YearDatePage.yearDateYear()).getValue()).to.contain('');

      $(YearDatePage.submit()).click();

      expect($(SummaryPage.yearDateExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
      expect($(SummaryPage.yearDateExclusiveAnswer()).getText()).to.not.have.string('2018');
    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive year date answer and removes focus, Then only the non-exclusive year date answer should be answered.', function() {
      // Given
      $(YearDatePage.yearDateExclusiveIPreferNotToSay()).click();
      expect($(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      $(YearDatePage.yearDateYear()).setValue('2018');

      // Then
      expect($(YearDatePage.yearDateYear()).getValue()).to.contain('2018');
      expect($(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(YearDatePage.submit()).click();

      expect($(SummaryPage.yearDateAnswer()).getText()).to.have.string('2018');
      expect($(SummaryPage.yearDateAnswer()).getText()).to.not.have.string('I prefer not to say');
    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive year date answer, Then only the non-exclusive year date answer should be answered.', function() {
      // Given
      expect($(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(YearDatePage.yearDateYear()).setValue('2018');

      // Then
      expect($(YearDatePage.yearDateYear()).getValue()).to.contain('2018');
      expect($(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(YearDatePage.submit()).click();

      expect($(SummaryPage.yearDateAnswer()).getText()).to.have.string('2018');
      expect($(SummaryPage.yearDateAnswer()).getText()).to.not.have.string('I prefer not to say');
    });
  });

  describe('Given the user has not answered the non-exclusive year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      // Given
      expect($(YearDatePage.yearDateYear()).getValue()).to.contain('');

      // When
      $(YearDatePage.yearDateExclusiveIPreferNotToSay()).click();
      expect($(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      $(YearDatePage.submit()).click();

      expect($(SummaryPage.yearDateExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
      expect($(SummaryPage.yearDateExclusiveAnswer()).getText()).to.not.have.string('2018');
    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      // Given
      expect($(YearDatePage.yearDateYear()).getValue()).to.contain('');
      expect($(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(YearDatePage.submit()).click();

      // Then
      expect($(SummaryPage.yearDateAnswer()).getText()).to.contain('No answer provided');
    });
  });
});
