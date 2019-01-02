import {openQuestionnaire} from '../../../../helpers/helpers.js'

const CurrencyPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-currency-section-summary.page');

describe('Component: Mutually Exclusive Currency With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
    cy.navigationLink('Currency').click();
  });

  describe('Given the user has entered a value for the non-exclusive currency answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(CurrencyPage.currency()).type('123')
        .get(CurrencyPage.currency()).invoke('val').should('contain', '123')

        // When
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).click()

        // Then
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).should('be.checked')
        .get(CurrencyPage.currency()).invoke('val').should('contain', '')

        .get(CurrencyPage.submit()).click()

        .get(SummaryPage.currencyExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.currencyExclusiveAnswer()).stripText().should('not.have.string', '123');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive currency answer and removes focus, Then only the non-exclusive currency answer should be answered.', function() {
      cy
        // Given
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).click()
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).should('be.checked')

        // When
        .get(CurrencyPage.currency()).type('123')

        // Then
        .get(CurrencyPage.currency()).invoke('val').should('contain', '123')
        .get(CurrencyPage.currencyLabel()).click()
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(CurrencyPage.submit()).click()

        .get(SummaryPage.currencyAnswer()).stripText().should('have.string', '123')
        .get(SummaryPage.currencyAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive currency answer, Then only the non-exclusive currency answer should be answered.', function() {
      cy
        // Given
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(CurrencyPage.currency()).type('123')

        // Then
        .get(CurrencyPage.currency()).invoke('val').should('contain', '123')
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(CurrencyPage.submit()).click()

        .get(SummaryPage.currencyAnswer()).stripText().should('have.string', '123')
        .get(SummaryPage.currencyAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive currency answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(CurrencyPage.currency()).invoke('val').should('contain', '')

        // When
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).click()
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(CurrencyPage.submit()).click()

        .get(SummaryPage.currencyExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.currencyExclusiveAnswer()).stripText().should('not.have.string', '123');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      cy
        // Given
        .get(CurrencyPage.currency()).invoke('val').should('contain', '')
        .get(CurrencyPage.currencyExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(CurrencyPage.submit()).click()

        // Then
        .get(SummaryPage.currencyAnswer()).stripText().should('contain', 'No answer provided');
    });
  });

});
