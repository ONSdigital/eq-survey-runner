import {openQuestionnaire} from '../../../../helpers/helpers.js';

const TextFieldPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-textfield.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-textfield-section-summary.page');

describe('Component: Mutually Exclusive Textfield With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
      .navigationLink('Textfield').click();
  });

  describe('Given the user has entered a value for the non-exclusive textfield answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(TextFieldPage.textfield()).type('Blue')
        .get(TextFieldPage.textfield()).invoke('val').should('contain', 'Blue')

        // When
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click()

        // Then
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should('be.checked')
        .get(TextFieldPage.textfield()).invoke('val').should('contain', '')

        .get(TextFieldPage.submit()).click()

        .get(SummaryPage.textfieldExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.textfieldExclusiveAnswer()).stripText().should('not.have.string', 'Blue');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.', function() {
      cy
        // Given
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click()
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should('be.checked')

        // When
        .get(TextFieldPage.textfield()).type('Blue')

        // Then
        .get(TextFieldPage.textfield()).invoke('val').should('contain', 'Blue')
        .get(TextFieldPage.textfieldLabel()).click()
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(TextFieldPage.submit()).click()

        .get(SummaryPage.textfieldAnswer()).stripText().should('have.string', 'Blue')
        .get(SummaryPage.textfieldAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textfield answer, Then only the non-exclusive textfield answer should be answered.', function() {
      cy
        // Given
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(TextFieldPage.textfield()).type('Blue')

        // Then
        .get(TextFieldPage.textfield()).invoke('val').should('contain', 'Blue')
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(TextFieldPage.submit()).click()

        .get(SummaryPage.textfieldAnswer()).stripText().should('have.string', 'Blue')
        .get(SummaryPage.textfieldAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive textfield answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(TextFieldPage.textfield()).invoke('val').should('contain', '')

        // When
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click()
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(TextFieldPage.submit()).click()

        .get(SummaryPage.textfieldExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.textfieldExclusiveAnswer()).stripText().should('not.have.string', 'Blue');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      cy
        // Given
        .get(TextFieldPage.textfield()).invoke('val').should('contain', '')
        .get(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(TextFieldPage.submit()).click()

        // Then
        .get(SummaryPage.textfieldAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
