import {openQuestionnaire} from '../../../../helpers/helpers.js';

const PercentagePage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-percentage.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-percentage-section-summary.page');

describe('Component: Mutually Exclusive Percentage With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
      .navigationLink('Percentage').click();
  });

  describe('Given the user has entered a value for the non-exclusive percentage answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(PercentagePage.percentage()).type('99')
        .get(PercentagePage.percentage()).invoke('val').should('contain', '99')

        // When
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).click()

        // Then
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).should('be.checked')
        .get(PercentagePage.percentage()).invoke('val').should('contain', '')

        .get(PercentagePage.submit()).click()

        .get(SummaryPage.percentageExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.percentageExclusiveAnswer()).stripText().should('not.have.string', '99');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive percentage answer and removes focus, Then only the non-exclusive percentage answer should be answered.', function() {
      cy
        // Given
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).click()
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).should('be.checked')

        // When
        .get(PercentagePage.percentage()).type('99')

        // Then
        .get(PercentagePage.percentage()).invoke('val').should('contain', '99')
        .get(PercentagePage.percentageLabel()).click()
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(PercentagePage.submit()).click()

        .get(SummaryPage.percentageAnswer()).stripText().should('have.string', '99')
        .get(SummaryPage.percentageAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive percentage answer, Then only the non-exclusive percentage answer should be answered.', function() {
      cy
        // Given
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(PercentagePage.percentage()).type('99')

        // Then
        .get(PercentagePage.percentage()).invoke('val').should('contain', '99')
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(PercentagePage.submit()).click()

        .get(SummaryPage.percentageAnswer()).stripText().should('have.string', '99')
        .get(SummaryPage.percentageAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive percentage answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(PercentagePage.percentage()).invoke('val').should('contain', '')

        // When
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).click()
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(PercentagePage.submit()).click()

        .get(SummaryPage.percentageExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.percentageExclusiveAnswer()).stripText().should('not.have.string', 'British\nIrish');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      cy
        // Given
        .get(PercentagePage.percentage()).invoke('val').should('contain', '')
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(PercentagePage.submit()).click()

        // Then
        .get(SummaryPage.percentageAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
