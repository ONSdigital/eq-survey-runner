import {openQuestionnaire} from '../../../../helpers/helpers.js';

const NumberPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-number.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-number-section-summary.page');

describe('Component: Mutually Exclusive Number With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
      .navigationLink('Number').click();
  });

  describe('Given the user has entered a value for the non-exclusive number answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(NumberPage.number()).type('123')
        .get(NumberPage.number()).invoke('val').should('contain', '123')

        // When
        .get(NumberPage.numberExclusiveIPreferNotToSay()).click()

        // Then
        .get(NumberPage.numberExclusiveIPreferNotToSay()).should('be.checked')
        .get(NumberPage.number()).invoke('val').should('contain', '')

        .get(NumberPage.submit()).click()

        .get(SummaryPage.numberExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.numberExclusiveAnswer()).stripText().should('not.have.string', '123');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive number answer and removes focus, Then only the non-exclusive number answer should be answered.', function() {
      cy
        // Given
        .get(NumberPage.numberExclusiveIPreferNotToSay()).click()
        .get(NumberPage.numberExclusiveIPreferNotToSay()).should('be.checked')

        // When
        .get(NumberPage.number()).type('123')

        // Then
        .get(NumberPage.number()).invoke('val').should('contain', '123')
        .get(NumberPage.numberLabel()).click()
        .get(NumberPage.numberExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(NumberPage.submit()).click()

        .get(SummaryPage.numberAnswer()).stripText().should('have.string', '123')
        .get(SummaryPage.numberAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive number answer, Then only the non-exclusive number answer should be answered.', function() {
      cy
        // Given
        .get(NumberPage.numberExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(NumberPage.number()).type('123')

        // Then
        .get(NumberPage.number()).invoke('val').should('contain', '123')
        .get(NumberPage.numberExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(NumberPage.submit()).click()

        .get(SummaryPage.numberAnswer()).stripText().should('have.string', '123')
        .get(SummaryPage.numberAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive number answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(NumberPage.number()).invoke('val').should('contain', '')

        // When
        .get(NumberPage.numberExclusiveIPreferNotToSay()).click()
        .get(NumberPage.numberExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(NumberPage.submit()).click()

        .get(SummaryPage.numberExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.numberExclusiveAnswer()).stripText().should('not.have.string', '123');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      cy
        // Given
        .get(NumberPage.number()).invoke('val').should('contain', '')
        .get(NumberPage.numberExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(NumberPage.submit()).click()

        // Then
        .get(SummaryPage.numberAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
