const helpers = require('../../../../helpers');

const PercentagePage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-percentage.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-percentage-section-summary.page');

describe('Component: Mutually Exclusive Percentage With Single Checkbox Override', function() {
  let browser;

  beforeEach(function() {
    helpers.openQuestionnaire('test_mutually_exclusive.json')
    .then(openBrowser => browser = openBrowser)
    .then(function() {
        browser.url('/questionnaire/mutually-exclusive-percentage');
    });
  });

  describe('Given the user has entered a value for the non-exclusive percentage answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

        // Given
        $(PercentagePage.percentage()).setValue('99');
        expect($(PercentagePage.percentage()).getValue()).to.contain('99');

        // When
        $(PercentagePage.percentageExclusiveIPreferNotToSay()).click();

        // Then
        expect($(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).to.be.true;
        expect($(PercentagePage.percentage()).getValue()).to.contain('');

        $(PercentagePage.submit()).click();

        expect($(SummaryPage.percentageExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.percentageExclusiveAnswer()).getText()).to.not.have.string('99');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive percentage answer and removes focus, Then only the non-exclusive percentage answer should be answered.', function() {

        // Given
        $(PercentagePage.percentageExclusiveIPreferNotToSay()).click();
        expect($(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // When
        $(PercentagePage.percentage()).setValue('99');

        // Then
        expect($(PercentagePage.percentage()).getValue()).to.contain('99');
        expect($(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(PercentagePage.submit()).click();

        expect($(SummaryPage.percentageAnswer()).getText()).to.have.string('99');
        expect($(SummaryPage.percentageAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive percentage answer, Then only the non-exclusive percentage answer should be answered.', function() {

        // Given
        expect($(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(PercentagePage.percentage()).setValue('99');

        // Then
        expect($(PercentagePage.percentage()).getValue()).to.contain('99');
        expect($(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(PercentagePage.submit()).click();

        expect($(SummaryPage.percentageAnswer()).getText()).to.have.string('99');
        expect($(SummaryPage.percentageAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive percentage answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

        // Given
        expect($(PercentagePage.percentage()).getValue()).to.contain('');

        // When
        $(PercentagePage.percentageExclusiveIPreferNotToSay()).click();
        expect($(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // Then
        $(PercentagePage.submit()).click();

        expect($(SummaryPage.percentageExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.percentageExclusiveAnswer()).getText()).to.not.have.string('British\nIrish');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

        // Given
        expect($(PercentagePage.percentage()).getValue()).to.contain('');
        expect($(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(PercentagePage.submit()).click();

        // Then
        expect($(SummaryPage.percentageAnswer()).getText()).to.contain('No answer provided');

    });
  });

});
