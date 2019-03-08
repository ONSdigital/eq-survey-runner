const helpers = require('../../../../helpers');

const TextFieldPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-textarea.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-textarea-section-summary.page');

describe('Component: Mutually Exclusive TextArea With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-textarea');
        });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textarea answer, Then only the non-exclusive textarea answer should be answered.', function() {

      return browser
        // Given
        .isSelected(TextFieldPage.textareaExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(TextFieldPage.textarea(), 'Blue')

        // Then
        .getValue(TextFieldPage.textarea()).should.eventually.contain('Blue')
        .isSelected(TextFieldPage.textareaExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(TextFieldPage.submit())

        .getText(SummaryPage.textareaAnswer()).should.eventually.have.string('Blue')
        .getText(SummaryPage.textareaAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive textarea answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(TextFieldPage.textarea()).should.eventually.contain('')

        // When
        .click(TextFieldPage.textareaExclusiveIPreferNotToSay())
        .isSelected(TextFieldPage.textareaExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(TextFieldPage.submit())

        .getText(SummaryPage.textareaExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.textareaExclusiveAnswer()).should.not.eventually.have.string('Blue');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(TextFieldPage.textarea()).should.eventually.contain('')
        .isSelected(TextFieldPage.textareaExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(TextFieldPage.submit())

        // Then
        .getText(SummaryPage.textareaAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
