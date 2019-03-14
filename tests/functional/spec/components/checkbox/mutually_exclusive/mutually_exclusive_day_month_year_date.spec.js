const helpers = require('../../../../helpers');

const DatePage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-date.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-date-section-summary.page');

describe('Component: Mutually Exclusive Day Month Year Date With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-date');
        });
  });

  describe('Given the user has entered a value for the non-exclusive month year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .setValue(DatePage.dateday(), '17')
        .selectByValue(DatePage.datemonth(), 3)
        .setValue(DatePage.dateyear(), '2018')
        .getValue(DatePage.dateday()).should.eventually.contain('17')
        .getText(DatePage.datemonth()).should.eventually.contain('March')
        .getValue(DatePage.dateyear()).should.eventually.contain('2018')

        // When
        .click(DatePage.dateExclusiveIPreferNotToSay())

        // Then
        .isSelected(DatePage.dateExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(DatePage.dateyear()).should.eventually.contain('')
        .getValue(DatePage.datemonth()).should.eventually.contain('')
        .getValue(DatePage.dateyear()).should.eventually.contain('')

        .click(DatePage.submit())

        .getText(SummaryPage.dateExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.dateExclusiveAnswer()).should.not.eventually.have.string('17 March 2018');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', function() {

      return browser
        // Given
        .click(DatePage.dateExclusiveIPreferNotToSay())
        .isSelected(DatePage.dateExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .setValue(DatePage.dateday(), '17')
        .selectByValue(DatePage.datemonth(), 3)
        .setValue(DatePage.dateyear(), '2018')

        // Then
        .getValue(DatePage.dateday()).should.eventually.contain('17')
        .getText(DatePage.datemonth()).should.eventually.contain('March')
        .getValue(DatePage.dateyear()).should.eventually.contain('2018')

        .isSelected(DatePage.dateExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(DatePage.submit())

        .getText(SummaryPage.dateAnswer()).should.eventually.have.string('17 March 2018')
        .getText(SummaryPage.dateAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', function() {

      return browser
        // Given
        .isSelected(DatePage.dateExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(DatePage.dateday(), '17')
        .selectByValue(DatePage.datemonth(), 3)
        .setValue(DatePage.dateyear(), '2018')

        // Then
        .getValue(DatePage.dateday()).should.eventually.contain('17')
        .getText(DatePage.datemonth()).should.eventually.contain('March')
        .getValue(DatePage.dateyear()).should.eventually.contain('2018')
        .isSelected(DatePage.dateExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(DatePage.submit())

        .getText(SummaryPage.dateAnswer()).should.eventually.have.string('17 March 2018')
        .getText(SummaryPage.dateAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive month year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(DatePage.dateyear()).should.eventually.contain('')
        .getValue(DatePage.datemonth()).should.eventually.contain('')
        .getValue(DatePage.dateyear()).should.eventually.contain('')

        // When
        .click(DatePage.dateExclusiveIPreferNotToSay())
        .isSelected(DatePage.dateExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(DatePage.submit())

        .getText(SummaryPage.dateExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.dateExclusiveAnswer()).should.not.eventually.have.string('17 March 2018');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(DatePage.dateyear()).should.eventually.contain('')
        .getValue(DatePage.datemonth()).should.eventually.contain('')
        .getValue(DatePage.dateyear()).should.eventually.contain('')
        .isSelected(DatePage.dateExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(DatePage.submit())

        // Then
        .getText(SummaryPage.dateAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
