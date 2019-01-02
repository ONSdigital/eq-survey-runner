import {openQuestionnaire} from '../../../../helpers/helpers.js'

const TextFieldPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-textarea.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-textarea-section-summary.page');

describe('Component: Mutually Exclusive TextArea With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
      .navigationLink('TextArea').click();
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textarea answer, Then only the non-exclusive textarea answer should be answered.', function() {
      cy
        // Given
        .get(TextFieldPage.textareaExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(TextFieldPage.textarea()).type('Blue')

        // Then
        .get(TextFieldPage.textarea()).invoke('val').should('contain', 'Blue')
        .get(TextFieldPage.textareaExclusiveIPreferNotToSay()).should('not.be.checked')

        .get(TextFieldPage.submit()).click()

        .get(SummaryPage.textareaAnswer()).stripText().should('have.string', 'Blue')
        .get(SummaryPage.textareaAnswer()).stripText().should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive textarea answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {
      cy
        // Given
        .get(TextFieldPage.textarea()).invoke('val').should('contain', '')

        // When
        .get(TextFieldPage.textareaExclusiveIPreferNotToSay()).click()
        .get(TextFieldPage.textareaExclusiveIPreferNotToSay()).should('be.checked')

        // Then
        .get(TextFieldPage.submit()).click()

        .get(SummaryPage.textareaExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.textareaExclusiveAnswer()).stripText().should('not.have.string', 'Blue');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {
      cy
        // Given
        .get(TextFieldPage.textarea()).invoke('val').should('contain', '')
        .get(TextFieldPage.textareaExclusiveIPreferNotToSay()).should('not.be.checked')

        // When
        .get(TextFieldPage.submit()).click()

        // Then
        .get(SummaryPage.textareaAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
