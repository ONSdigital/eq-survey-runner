import {openQuestionnaire} from '../../../../helpers/helpers.js';

const UnitPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-unit-section-summary.page');

describe('Component: Mutually Exclusive Unit With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
      .navigationLink('Unit').click();
  });

  describe('Given the user has entered a value for the non-exclusive unit answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(UnitPage.unit()).type('10')
        .get(UnitPage.unit()).invoke('val').should('contain', '10')

        // When
        .get(UnitPage.unitExclusiveIPreferNotToSay()).click()

        // Then
        .get(UnitPage.unitExclusiveIPreferNotToSay()).should('be.checked')
        .get(UnitPage.unit()).invoke('val').should('contain', '')

        .get(UnitPage.submit()).click()

        .get(SummaryPage.unitExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.unitExclusiveAnswer()).stripText().should('not.have.string', '10');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive unit answer and removes focus, Then only the non-exclusive unit answer should be answered.', function() {
      cy
        // Given
        .get(UnitPage.unitExclusiveIPreferNotToSay()).click()
        .get(UnitPage.unitExclusiveIPreferNotToSay()).should('be.checked')

        // When
        .get(UnitPage.unit()).type('10')

        // Then
        .get(UnitPage.unit()).invoke('val').should('contain', '10')
        .get(UnitPage.unitLabel()).click()
        .get(UnitPage.unitExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(UnitPage.submit()).click()

        .get(SummaryPage.unitAnswer()).stripText().should('have.string', '10')
        .get(SummaryPage.unitAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive unit answer, Then only the non-exclusive unit answer should be answered.', function() {
      cy
        // Given
        .get(UnitPage.unitExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(UnitPage.unit()).type('10')

        // Then
        .get(UnitPage.unit()).invoke('val').should('contain', '10')
        .get(UnitPage.unitExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(UnitPage.submit()).click()

        .get(SummaryPage.unitAnswer()).stripText().should('have.string', '10')
        .get(SummaryPage.unitAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive unit answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(UnitPage.unit()).invoke('val').should('contain', '')

        // When
        .get(UnitPage.unitExclusiveIPreferNotToSay()).click()
        .get(UnitPage.unitExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(UnitPage.submit()).click()

        .get(SummaryPage.unitExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.unitExclusiveAnswer()).stripText().should('not.have.string', '10');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      cy
        // Given
        .get(UnitPage.unit()).invoke('val').should('contain', '')
        .get(UnitPage.unitExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(UnitPage.submit()).click()

        // Then
        .get(SummaryPage.unitAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
