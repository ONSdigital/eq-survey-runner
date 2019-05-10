const helpers = require('../../../../helpers');

const TextFieldPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-textfield.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-textfield-section-summary.page');

describe('Component: Mutually Exclusive Textfield With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-textfield');
        });
  });

  describe('Given the user has entered a value for the non-exclusive textfield answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .setValue(TextFieldPage.textfield(), 'Blue')
        .getValue(TextFieldPage.textfield()).should.eventually.contain('Blue')

        // When
        .click(TextFieldPage.textfieldExclusiveIPreferNotToSay())

        // Then
        .isSelected(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(TextFieldPage.textfield()).should.eventually.contain('')

        .click(TextFieldPage.submit())

        .getText(SummaryPage.textfieldExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.textfieldExclusiveAnswer()).should.not.eventually.have.string('Blue');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.', function() {

      return browser
        // Given
        .click(TextFieldPage.textfieldExclusiveIPreferNotToSay())
        .isSelected(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .setValue(TextFieldPage.textfield(), 'Blue')

        // Then
        .getValue(TextFieldPage.textfield()).should.eventually.contain('Blue')
        .isSelected(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(TextFieldPage.submit())

        .getText(SummaryPage.textfieldAnswer()).should.eventually.have.string('Blue')
        .getText(SummaryPage.textfieldAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive textfield answer, Then only the non-exclusive textfield answer should be answered.', function() {

      return browser
        // Given
        .isSelected(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(TextFieldPage.textfield(), 'Blue')

        // Then
        .getValue(TextFieldPage.textfield()).should.eventually.contain('Blue')
        .isSelected(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(TextFieldPage.submit())

        .getText(SummaryPage.textfieldAnswer()).should.eventually.have.string('Blue')
        .getText(SummaryPage.textfieldAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive textfield answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(TextFieldPage.textfield()).should.eventually.contain('')

        // When
        .click(TextFieldPage.textfieldExclusiveIPreferNotToSay())
        .isSelected(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(TextFieldPage.submit())

        .getText(SummaryPage.textfieldExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.textfieldExclusiveAnswer()).should.not.eventually.have.string('Blue');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(TextFieldPage.textfield()).should.eventually.contain('')
        .isSelected(TextFieldPage.textfieldExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(TextFieldPage.submit())

        // Then
        .getText(SummaryPage.textfieldAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
