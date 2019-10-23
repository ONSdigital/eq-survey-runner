const helpers = require('../../../../helpers');

const TextFieldPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-textarea.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-textarea-section-summary.page');

describe('Component: Mutually Exclusive TextArea With Single Checkbox Override', function() {
  let browser;

  beforeEach(function() {
    browser = helpers.openQuestionnaire('test_mutually_exclusive.json')
    .then(openBrowser => browser = openBrowser)
    .then(function() {
      browser.url('/questionnaire/mutually-exclusive-textarea');
    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textarea answer, Then only the non-exclusive textarea answer should be answered.', function() {

        // Given
        expect($(TextFieldPage.textareaExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(TextFieldPage.textarea()).setValue('Blue');

        // Then
        expect($(TextFieldPage.textarea()).getValue()).to.contain('Blue');
        expect($(TextFieldPage.textareaExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(TextFieldPage.submit()).click();

        expect($(SummaryPage.textareaAnswer()).getText()).to.have.string('Blue');
        expect($(SummaryPage.textareaAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive textarea answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

        // Given
        expect($(TextFieldPage.textarea()).getValue()).to.contain('');

        // When
        $(TextFieldPage.textareaExclusiveIPreferNotToSay()).click();
        expect($(TextFieldPage.textareaExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // Then
        $(TextFieldPage.submit()).click();

        expect($(SummaryPage.textareaExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.textareaExclusiveAnswer()).getText()).to.not.have.string('Blue');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

        // Given
        expect($(TextFieldPage.textarea()).getValue()).to.contain('');
        expect($(TextFieldPage.textareaExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(TextFieldPage.submit()).click();

        // Then
        expect($(SummaryPage.textareaAnswer()).getText()).to.contain('No answer provided');

    });
  });

});
