import {openQuestionnaire} from ../../../../helpers/helpers.js

const TextFieldPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-textarea.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-textarea-section-summary.page');

describe('Component: Mutually Exclusive TextArea With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
          return browser.get(helpers.navigationLink('TextArea')).click();
        });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textarea answer, Then only the non-exclusive textarea answer should be answered.', function() {

              // Given
        .isSelected(TextFieldPage.textareaExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .get(TextFieldPage.textarea()).type('Blue')

        // Then
        .getValue(TextFieldPage.textarea()).should.eventually.contain('Blue')
        .isSelected(TextFieldPage.textareaExclusiveIPreferNotToSay()).should.eventually.be.false

        .get(TextFieldPage.submit()).click()

        .get(SummaryPage.textareaAnswer()).stripText().should('have.string', 'Blue')
        .get(SummaryPage.textareaAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive textarea answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

              // Given
        .getValue(TextFieldPage.textarea()).should.eventually.contain('')

        // When
        .get(TextFieldPage.textareaExclusiveIPreferNotToSay()).click()
        .isSelected(TextFieldPage.textareaExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .get(TextFieldPage.submit()).click()

        .get(SummaryPage.textareaExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.textareaExclusiveAnswer()).should('not.have.string', 'Blue');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

              // Given
        .getValue(TextFieldPage.textarea()).should.eventually.contain('')
        .isSelected(TextFieldPage.textareaExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .get(TextFieldPage.submit()).click()

        // Then
        .get(SummaryPage.textareaAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
