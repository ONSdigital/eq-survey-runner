const helpers = require('../../../../helpers');

const NumberPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-number.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-number-section-summary.page');

describe('Component: Mutually Exclusive Number With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-number');
        });
  });

  describe('Given the user has entered a value for the non-exclusive number answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .setValue(NumberPage.number(), '123')
        .getValue(NumberPage.number()).should.eventually.contain('123')

        // When
        .click(NumberPage.numberExclusiveIPreferNotToSay())

        // Then
        .isSelected(NumberPage.numberExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(NumberPage.number()).should.eventually.contain('')

        .click(NumberPage.submit())

        .getText(SummaryPage.numberExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.numberExclusiveAnswer()).should.not.eventually.have.string('123');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive number answer and removes focus, Then only the non-exclusive number answer should be answered.', function() {

      return browser
        // Given
        .click(NumberPage.numberExclusiveIPreferNotToSay())
        .isSelected(NumberPage.numberExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .setValue(NumberPage.number(), '123')

        // Then
        .getValue(NumberPage.number()).should.eventually.contain('123')
        .isSelected(NumberPage.numberExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(NumberPage.submit())

        .getText(SummaryPage.numberAnswer()).should.eventually.have.string('123')
        .getText(SummaryPage.numberAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive number answer, Then only the non-exclusive number answer should be answered.', function() {

      return browser
        // Given
        .isSelected(NumberPage.numberExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(NumberPage.number(), '123')

        // Then
        .getValue(NumberPage.number()).should.eventually.contain('123')
        .isSelected(NumberPage.numberExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(NumberPage.submit())

        .getText(SummaryPage.numberAnswer()).should.eventually.have.string('123')
        .getText(SummaryPage.numberAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive number answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(NumberPage.number()).should.eventually.contain('')

        // When
        .click(NumberPage.numberExclusiveIPreferNotToSay())
        .isSelected(NumberPage.numberExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(NumberPage.submit())

        .getText(SummaryPage.numberExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.numberExclusiveAnswer()).should.not.eventually.have.string('123');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(NumberPage.number()).should.eventually.contain('')
        .isSelected(NumberPage.numberExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(NumberPage.submit())

        // Then
        .getText(SummaryPage.numberAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
