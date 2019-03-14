const helpers = require('../../../../helpers');

const DurationPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-duration-section-summary.page');

describe('Component: Mutually Exclusive Duration With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-duration');
        });
  });

  describe('Given the user has entered a value for the non-exclusive duration answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .setValue(DurationPage.durationYears(), '1')
        .setValue(DurationPage.durationMonths(), '7')

        .getValue(DurationPage.durationYears()).should.eventually.contain('1')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('7')

        // When
        .click(DurationPage.durationExclusiveIPreferNotToSay())

        // Then
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(DurationPage.durationYears()).should.eventually.contain('')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('')

        .click(DurationPage.submit())

        .getText(SummaryPage.durationExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.durationExclusiveAnswer()).should.not.eventually.have.string('1 year 7 months');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive duration answer and removes focus, Then only the non-exclusive duration answer should be answered.', function() {

      return browser
        // Given
        .click(DurationPage.durationExclusiveIPreferNotToSay())
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .setValue(DurationPage.durationYears(), '1')
        .setValue(DurationPage.durationMonths(), '7')

        // Then
        .getValue(DurationPage.durationYears()).should.eventually.contain('1')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('7')
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(DurationPage.submit())

        .getText(SummaryPage.durationAnswer()).should.eventually.have.string('1 year 7 months')
        .getText(SummaryPage.durationAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive duration answer, Then only the non-exclusive duration answer should be answered.', function() {

      return browser
        // Given
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .setValue(DurationPage.durationYears(), '1')
        .setValue(DurationPage.durationMonths(), '7')

        // Then
        .getValue(DurationPage.durationYears()).should.eventually.contain('1')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('7')
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(DurationPage.submit())

        .getText(SummaryPage.durationAnswer()).should.eventually.have.string('1 year 7 months')
        .getText(SummaryPage.durationAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive duration answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(DurationPage.durationYears()).should.eventually.contain('')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('')

        // When
        .click(DurationPage.durationExclusiveIPreferNotToSay())
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(DurationPage.submit())

        .getText(SummaryPage.durationExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.durationExclusiveAnswer()).should.not.eventually.have.string('1 year 7 months');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(DurationPage.durationYears()).should.eventually.contain('')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('')
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(DurationPage.submit())

        // Then
        .getText(SummaryPage.durationAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
