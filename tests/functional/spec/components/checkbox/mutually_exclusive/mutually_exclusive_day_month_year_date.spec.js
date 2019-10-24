const helpers = require('../../../../helpers');

const DatePage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-date.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-date-section-summary.page');

describe('Component: Mutually Exclusive Day Month Year Date With Single Checkbox Override', function() {
  let browser;

  beforeEach(function() {
    helpers.openQuestionnaire('test_mutually_exclusive.json')
    .then(openBrowser => browser = openBrowser)
    .then(function() {
        browser.url('/questionnaire/mutually-exclusive-date');
    });
  });

  describe('Given the user has entered a value for the non-exclusive month year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {
        // Given
        $(DatePage.dateday()).setValue('17');
        $(DatePage.datemonth()).setValue('3');
        $(DatePage.dateyear()).setValue('2018');
        expect($(DatePage.dateday()).getValue()).to.contain('17');
        expect($(DatePage.datemonth()).getValue()).to.contain('3');
        expect($(DatePage.dateyear()).getValue()).to.contain('2018');

        // When
        $(DatePage.dateExclusiveIPreferNotToSay()).click();

        // Then
        expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
        expect($(DatePage.dateday()).getValue()).to.contain('');
        expect($(DatePage.datemonth()).getValue()).to.contain('');
        expect($(DatePage.dateyear()).getValue()).to.contain('');

        $(DatePage.submit()).click();

        expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string('17 March 2018');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', function() {

        // Given
        $(DatePage.dateExclusiveIPreferNotToSay()).click();
        expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // When
        $(DatePage.dateday()).setValue('17');
        $(DatePage.datemonth()).setValue('3');
        $(DatePage.dateyear()).setValue('2018');

        // Then
        expect($(DatePage.dateday()).getValue()).to.contain('17');
        expect($(DatePage.datemonth()).getValue()).to.contain('3');
        expect($(DatePage.dateyear()).getValue()).to.contain('2018');

        expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(DatePage.submit()).click();

        expect($(SummaryPage.dateAnswer()).getText()).to.have.string('17 March 2018');
        expect($(SummaryPage.dateAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', function() {

        // Given
        expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(DatePage.dateday()).setValue('17');
        $(DatePage.datemonth()).setValue('3');
        $(DatePage.dateyear()).setValue('2018');

        // Then
        expect($(DatePage.dateday()).getValue()).to.contain('17');
        expect($(DatePage.datemonth()).getValue()).to.contain('3');
        expect($(DatePage.dateyear()).getValue()).to.contain('2018');
        expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(DatePage.submit()).click();

        expect($(SummaryPage.dateAnswer()).getText()).to.have.string('17 March 2018');
        expect($(SummaryPage.dateAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive month year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

        // Given
        expect($(DatePage.dateday()).getValue()).to.contain('');
        expect($(DatePage.datemonth()).getValue()).to.contain('');
        expect($(DatePage.dateyear()).getValue()).to.contain('');

        // When
        $(DatePage.dateExclusiveIPreferNotToSay()).click();
        expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // Then
        $(DatePage.submit()).click();

        expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string('17 March 2018');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

        // Given
        expect($(DatePage.dateday()).getValue()).to.contain('');
        expect($(DatePage.datemonth()).getValue()).to.contain('');
        expect($(DatePage.dateyear()).getValue()).to.contain('');
        expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(DatePage.submit()).click();

        // Then
        expect($(SummaryPage.dateAnswer()).getText()).to.contain('No answer provided');
    });
  });
});
