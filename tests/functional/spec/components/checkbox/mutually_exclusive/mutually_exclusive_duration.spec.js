const helpers = require('../../../../helpers');

const DurationPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-duration-section-summary.page');

describe('Component: Mutually Exclusive Duration With Single Checkbox Override', function() {
  let browser;

  beforeEach(function() {
    browser = helpers.openQuestionnaire('test_mutually_exclusive.json')
    .then(openBrowser => browser = openBrowser)
    .then(function() {
        browser.url('/questionnaire/mutually-exclusive-duration');
    });
  });

  describe('Given the user has entered a value for the non-exclusive duration answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

        // Given
        $(DurationPage.durationYears()).setValue('1');
        $(DurationPage.durationMonths()).setValue('7');

        expect($(DurationPage.durationYears()).getValue()).to.contain('1');
        expect($(DurationPage.durationMonths()).getValue()).to.contain('7');

        // When
        $(DurationPage.durationExclusiveIPreferNotToSay()).click();

        // Then
        expect($(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;
        expect($(DurationPage.durationYears()).getValue()).to.contain('');
        expect($(DurationPage.durationMonths()).getValue()).to.contain('');

        $(DurationPage.submit()).click();

        expect($(SummaryPage.durationExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.durationExclusiveAnswer()).getText()).to.not.have.string('1 year 7 months');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive duration answer and removes focus, Then only the non-exclusive duration answer should be answered.', function() {

        // Given
        $(DurationPage.durationExclusiveIPreferNotToSay()).click();
        expect($(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // When
        $(DurationPage.durationYears()).setValue('1');
        $(DurationPage.durationMonths()).setValue('7');

        // Then
        expect($(DurationPage.durationYears()).getValue()).to.contain('1');
        expect($(DurationPage.durationMonths()).getValue()).to.contain('7');
        expect($(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(DurationPage.submit()).click();

        expect($(SummaryPage.durationAnswer()).getText()).to.have.string('1 year 7 months');
        expect($(SummaryPage.durationAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive duration answer, Then only the non-exclusive duration answer should be answered.', function() {

        // Given
        expect($(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(DurationPage.durationYears()).setValue('1');
        $(DurationPage.durationMonths()).setValue('7');

        // Then
        expect($(DurationPage.durationYears()).getValue()).to.contain('1');
        expect($(DurationPage.durationMonths()).getValue()).to.contain('7');
        expect($(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(DurationPage.submit()).click();

        expect($(SummaryPage.durationAnswer()).getText()).to.have.string('1 year 7 months');
        expect($(SummaryPage.durationAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive duration answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

        // Given
        expect($(DurationPage.durationYears()).getValue()).to.contain('');
        expect($(DurationPage.durationMonths()).getValue()).to.contain('');

        // When
        $(DurationPage.durationExclusiveIPreferNotToSay()).click();
        expect($(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // Then
        $(DurationPage.submit()).click();

        expect($(SummaryPage.durationExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.durationExclusiveAnswer()).getText()).to.not.have.string('1 year 7 months');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

        // Given
        expect($(DurationPage.durationYears()).getValue()).to.contain('');
        expect($(DurationPage.durationMonths()).getValue()).to.contain('');
        expect($(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(DurationPage.submit()).click();

        // Then
        expect($(SummaryPage.durationAnswer()).getText()).to.contain('No answer provided');

    });
  });

});
