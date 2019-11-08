const CurrencyPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-currency-section-summary.page');

describe('Component: Mutually Exclusive Currency With Single Checkbox Override', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_mutually_exclusive.json');
    browser.url('/questionnaire/mutually-exclusive-currency');
  });

  describe('Given the user has entered a value for the non-exclusive currency answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      // Given
      $(CurrencyPage.currency()).setValue('123');
      expect($(CurrencyPage.currency()).getValue()).to.contain('123');

      // When
      $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();

      // Then
      expect($(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(CurrencyPage.currency()).getValue()).to.contain('');

      $(CurrencyPage.submit()).click();

      expect($(SummaryPage.currencyExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
      expect($(SummaryPage.currencyExclusiveAnswer()).getText()).to.not.have.string('123');
    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive currency answer and removes focus, Then only the non-exclusive currency answer should be answered.', function() {
      // Given
      $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();
      expect($(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      $(CurrencyPage.currency()).setValue('123');

      // Then
      $(CurrencyPage.currency()).getValue();
      expect($(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(CurrencyPage.submit()).click();

      expect($(SummaryPage.currencyAnswer()).getText()).to.have.string('123');
      expect($(SummaryPage.currencyAnswer()).getText()).to.not.have.string('I prefer not to say');
    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive currency answer, Then only the non-exclusive currency answer should be answered.', function() {
      // Given
      expect($(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(CurrencyPage.currency()).setValue('123');

      // Then
      expect($(CurrencyPage.currency()).getValue()).to.contain('123');
      expect($(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(CurrencyPage.submit()).click();

      expect($(SummaryPage.currencyAnswer()).getText()).to.have.string('123');
      expect($(SummaryPage.currencyAnswer()).getText()).to.not.have.string('I prefer not to say');
    });
  });

  describe('Given the user has not answered the non-exclusive currency answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      // Given
      expect($(CurrencyPage.currency()).getValue()).to.contain('');

      // When
      $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();
      expect($(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      $(CurrencyPage.submit()).click();

      expect($(SummaryPage.currencyExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
      expect($(SummaryPage.currencyExclusiveAnswer()).getText()).to.not.have.string('123');
    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      // Given
      expect($(CurrencyPage.currency()).getValue()).to.contain('');
      expect($(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(CurrencyPage.submit()).click();

      // Then
      expect($(SummaryPage.currencyAnswer()).getText()).to.contain('No answer provided');
    });
  });
});
