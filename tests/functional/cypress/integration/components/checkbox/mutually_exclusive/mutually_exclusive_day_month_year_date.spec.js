import {openQuestionnaire} from '../../../../helpers/helpers.js';

const DatePage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-date.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-date-section-summary.page');

describe('Component: Mutually Exclusive Day Month Year Date With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json');
    cy.navigationLink('Date').click();
  });

  describe('Given the user has entered a value for the non-exclusive month year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(DatePage.dateday()).type('17')
        .get(DatePage.datemonth()).select('3')
        .get(DatePage.dateyear()).type('2018')
        .get(DatePage.dateday()).invoke('val').should('contain', '17')
        .get(DatePage.datemonth()).stripText().should('contain', 'March')
        .get(DatePage.dateyear()).invoke('val').should('contain', '2018')

        // When
        .get(DatePage.dateExclusiveIPreferNotToSay()).click()

        // Then
        .get(DatePage.dateExclusiveIPreferNotToSay()).should('be.checked')
        .get(DatePage.dateyear()).invoke('val').should('contain', '')
        .get(DatePage.datemonth()).invoke('val').should('contain', '')
        .get(DatePage.dateyear()).invoke('val').should('contain', '')

        .get(DatePage.submit()).click()

        .get(SummaryPage.dateExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.dateExclusiveAnswer()).stripText().should('not.have.string', '17 March 2018');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', function() {
      cy
        // Given
        .get(DatePage.dateExclusiveIPreferNotToSay()).click()
        .get(DatePage.dateExclusiveIPreferNotToSay()).should('be.checked')

        // When
        .get(DatePage.dateday()).type('17')
        .get(DatePage.datemonth()).select('3')
        .get(DatePage.dateyear()).type('2018')

        // Then
        .get(DatePage.dateday()).invoke('val').should('contain', '17')
        .get(DatePage.datemonth()).stripText().should('contain', 'March')
        .get(DatePage.dateyear()).invoke('val').should('contain', '2018')

        .get(DatePage.dateExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(DatePage.submit()).click()

        .get(SummaryPage.dateAnswer()).stripText().should('have.string', '17 March 2018')
        .get(SummaryPage.dateAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', function() {
      cy
        // Given
        .get(DatePage.dateExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(DatePage.dateday()).type('17')
        .get(DatePage.datemonth()).select('3')
        .get(DatePage.dateyear()).type('2018')

        // Then
        .get(DatePage.dateday()).invoke('val').should('contain', '17')
        .get(DatePage.datemonth()).stripText().should('contain', 'March')
        .get(DatePage.dateyear()).invoke('val').should('contain', '2018')
        .get(DatePage.dateExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(DatePage.submit()).click()

        .get(SummaryPage.dateAnswer()).stripText().should('have.string', '17 March 2018')
        .get(SummaryPage.dateAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive month year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(DatePage.dateyear()).invoke('val').should('contain', '')
        .get(DatePage.datemonth()).invoke('val').should('contain', '')
        .get(DatePage.dateyear()).invoke('val').should('contain', '')

        // When
        .get(DatePage.dateExclusiveIPreferNotToSay()).click()
        .get(DatePage.dateExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(DatePage.submit()).click()

        .get(SummaryPage.dateExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.dateExclusiveAnswer()).stripText().should('not.have.string', '17 March 2018');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      cy
        // Given
        .get(DatePage.dateyear()).invoke('val').should('contain', '')
        .get(DatePage.datemonth()).invoke('val').should('contain', '')
        .get(DatePage.dateyear()).invoke('val').should('contain', '')
        .get(DatePage.dateExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(DatePage.submit()).click()

        // Then
        .get(SummaryPage.dateAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
