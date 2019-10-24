const helpers = require('../../../../helpers');

const TextFieldPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-textfield.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-textfield-section-summary.page');

describe('Component: Mutually Exclusive Textfield With Single Checkbox Override', function() {
  let browser;

  beforeEach(function() {
    helpers.openQuestionnaire('test_mutually_exclusive.json')
    .then(openBrowser => browser = openBrowser)
    .then(function() {
      browser.url('/questionnaire/mutually-exclusive-textfield');
    });
  });

  describe('Given the user has entered a value for the non-exclusive textfield answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

        // Given
        $(TextFieldPage.textfield()).setValue('Blue');
        expect($(TextFieldPage.textfield()).getValue()).to.contain('Blue');

        // When
        $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();

        // Then
        expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;
        expect($(TextFieldPage.textfield()).getValue()).to.contain('');

        $(TextFieldPage.submit()).click();

        expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string('Blue');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.', function() {

        // Given
        $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
        expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // When
        $(TextFieldPage.textfield()).setValue('Blue');

        // Then
        expect($(TextFieldPage.textfield()).getValue()).to.contain('Blue');
        expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(TextFieldPage.submit()).click();

        expect($(SummaryPage.textfieldAnswer()).getText()).to.have.string('Blue');
        expect($(SummaryPage.textfieldAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textfield answer, Then only the non-exclusive textfield answer should be answered.', function() {

        // Given
        expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(TextFieldPage.textfield()).setValue('Blue');

        // Then
        expect($(TextFieldPage.textfield()).getValue()).to.contain('Blue');
        expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(TextFieldPage.submit()).click();

        expect($(SummaryPage.textfieldAnswer()).getText()).to.have.string('Blue');
        expect($(SummaryPage.textfieldAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive textfield answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

        // Given
        expect($(TextFieldPage.textfield()).getValue()).to.contain('');

        // When
        $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
        expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // Then
        $(TextFieldPage.submit()).click();

        expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string('Blue');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

        // Given
        expect($(TextFieldPage.textfield()).getValue()).to.contain('');
        expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(TextFieldPage.submit()).click();

        // Then
        expect($(SummaryPage.textfieldAnswer()).getText()).to.contain('No answer provided');

    });
  });

});
