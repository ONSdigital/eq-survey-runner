const helpers = require('../../../../helpers');

const CurrencyPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-currency-section-summary.page');

describe('Component: Mutually Exclusive Currency With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-currency');
        });
  });

  describe('Given the user has entered a value for the non-exclusive currency answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .setValue(CurrencyPage.currency(), '123')
        .getValue(CurrencyPage.currency()).should.eventually.contain('123')

        // When
        .click(CurrencyPage.currencyExclusiveIPreferNotToSay())

        // Then
        .isSelected(CurrencyPage.currencyExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(CurrencyPage.currency()).should.eventually.contain('')

        .click(CurrencyPage.submit())

        .getText(SummaryPage.currencyExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.currencyExclusiveAnswer()).should.not.eventually.have.string('123');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive currency answer and removes focus, Then only the non-exclusive currency answer should be answered.', function() {

      return browser
        // Given
        .click(CurrencyPage.currencyExclusiveIPreferNotToSay())
        .isSelected(CurrencyPage.currencyExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .setValue(CurrencyPage.currency(), '123')

        // Then
        .getValue(CurrencyPage.currency()).should.eventually.contain('123')
        .isSelected(CurrencyPage.currencyExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(CurrencyPage.submit())

        .getText(SummaryPage.currencyAnswer()).should.eventually.have.string('123')
        .getText(SummaryPage.currencyAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive currency answer, Then only the non-exclusive currency answer should be answered.', function() {

      return browser
        // Given
        .isSelected(CurrencyPage.currencyExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(CurrencyPage.currency(), '123')

        // Then
        .getValue(CurrencyPage.currency()).should.eventually.contain('123')
        .isSelected(CurrencyPage.currencyExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(CurrencyPage.submit())

        .getText(SummaryPage.currencyAnswer()).should.eventually.have.string('123')
        .getText(SummaryPage.currencyAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive currency answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(CurrencyPage.currency()).should.eventually.contain('')

        // When
        .click(CurrencyPage.currencyExclusiveIPreferNotToSay())
        .isSelected(CurrencyPage.currencyExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(CurrencyPage.submit())

        .getText(SummaryPage.currencyExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.currencyExclusiveAnswer()).should.not.eventually.have.string('123');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(CurrencyPage.currency()).should.eventually.contain('')
        .isSelected(CurrencyPage.currencyExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(CurrencyPage.submit())

        // Then
        .getText(SummaryPage.currencyAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
