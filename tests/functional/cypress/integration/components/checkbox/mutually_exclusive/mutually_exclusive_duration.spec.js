import {openQuestionnaire} from '../../../../helpers/helpers.js';

const DurationPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-duration-section-summary.page');

describe('Component: Mutually Exclusive Duration With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
      .navigationLink('Duration').click();
  });

  describe('Given the user has entered a value for the non-exclusive duration answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(DurationPage.durationYears()).type('1')
        .get(DurationPage.durationMonths()).type('7')

        .get(DurationPage.durationYears()).invoke('val').should('contain', '1')
        .get(DurationPage.durationMonths()).invoke('val').should('contain', '7')

        // When
        .get(DurationPage.durationExclusiveIPreferNotToSay()).click()

        // Then
        .get(DurationPage.durationExclusiveIPreferNotToSay()).should('be.checked')
        .get(DurationPage.durationYears()).invoke('val').should('contain', '')
        .get(DurationPage.durationMonths()).invoke('val').should('contain', '')

        .get(DurationPage.submit()).click()

        .get(SummaryPage.durationExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.durationExclusiveAnswer()).stripText().should('not.have.string', '1 year 7 months');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive duration answer and removes focus, Then only the non-exclusive duration answer should be answered.', function() {
      cy
        // Given
        .get(DurationPage.durationExclusiveIPreferNotToSay()).click()
        .get(DurationPage.durationExclusiveIPreferNotToSay()).should('be.checked')

        // When
        .get(DurationPage.durationYears()).type('1')
        .get(DurationPage.durationMonths()).type('7')

        // Then
        .get(DurationPage.durationYears()).invoke('val').should('contain', '1')
        .get(DurationPage.durationMonths()).invoke('val').should('contain', '7')
        .get(DurationPage.durationExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(DurationPage.submit()).click()

        .get(SummaryPage.durationAnswer()).stripText().should('have.string', '1 year 7 months')
        .get(SummaryPage.durationAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive duration answer, Then only the non-exclusive duration answer should be answered.', function() {
      cy
        // Given
        .get(DurationPage.durationExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(DurationPage.durationYears()).type('1')
        .get(DurationPage.durationMonths()).type('7')

        // Then
        .get(DurationPage.durationYears()).invoke('val').should('contain', '1')
        .get(DurationPage.durationMonths()).invoke('val').should('contain', '7')
        .get(DurationPage.durationExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(DurationPage.submit()).click()

        .get(SummaryPage.durationAnswer()).stripText().should('have.string', '1 year 7 months')
        .get(SummaryPage.durationAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive duration answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(DurationPage.durationYears()).invoke('val').should('contain', '')
        .get(DurationPage.durationMonths()).invoke('val').should('contain', '')

        // When
        .get(DurationPage.durationExclusiveIPreferNotToSay()).click()
        .get(DurationPage.durationExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(DurationPage.submit()).click()

        .get(SummaryPage.durationExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.durationExclusiveAnswer()).stripText().should('not.have.string', '1 year 7 months');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      cy
        // Given
        .get(DurationPage.durationYears()).invoke('val').should('contain', '')
        .get(DurationPage.durationMonths()).invoke('val').should('contain', '')
        .get(DurationPage.durationExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(DurationPage.submit()).click()

        // Then
        .get(SummaryPage.durationAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
