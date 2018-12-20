import {openQuestionnaire} from ../../../../helpers/helpers.js

const DurationPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-duration-section-summary.page');

describe('Component: Mutually Exclusive Duration With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
          return browser.get(helpers.navigationLink('Duration')).click();
        });
  });

  describe('Given the user has entered a value for the non-exclusive duration answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

              // Given
        .get(DurationPage.durationYears()).type('1')
        .get(DurationPage.durationMonths()).type('7')

        .getValue(DurationPage.durationYears()).should.eventually.contain('1')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('7')

        // When
        .get(DurationPage.durationExclusiveIPreferNotToSay()).click()

        // Then
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should('be.true')
        .getValue(DurationPage.durationYears()).should.eventually.contain('')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('')

        .get(DurationPage.submit()).click()

        .get(SummaryPage.durationExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.durationExclusiveAnswer()).should('not.have.string', '1 year 7 months');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive duration answer and removes focus, Then only the non-exclusive duration answer should be answered.', function() {

              // Given
        .get(DurationPage.durationExclusiveIPreferNotToSay()).click()
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should('be.true')

        // When
        .get(DurationPage.durationYears()).type('1')
        .get(DurationPage.durationMonths()).type('7')

        // Then
        .getValue(DurationPage.durationYears()).should.eventually.contain('1')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('7')
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should('be.false')

        .get(DurationPage.submit()).click()

        .get(SummaryPage.durationAnswer()).stripText().should('have.string', '1 year 7 months')
        .get(SummaryPage.durationAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive duration answer, Then only the non-exclusive duration answer should be answered.', function() {

              // Given
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should('be.false')

        // When
        .get(DurationPage.durationYears()).type('1')
        .get(DurationPage.durationMonths()).type('7')

        // Then
        .getValue(DurationPage.durationYears()).should.eventually.contain('1')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('7')
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should('be.false')

        .get(DurationPage.submit()).click()

        .get(SummaryPage.durationAnswer()).stripText().should('have.string', '1 year 7 months')
        .get(SummaryPage.durationAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive duration answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

              // Given
        .getValue(DurationPage.durationYears()).should.eventually.contain('')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('')

        // When
        .get(DurationPage.durationExclusiveIPreferNotToSay()).click()
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should('be.true')

        // Then
        .get(DurationPage.submit()).click()

        .get(SummaryPage.durationExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.durationExclusiveAnswer()).should('not.have.string', '1 year 7 months');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

              // Given
        .getValue(DurationPage.durationYears()).should.eventually.contain('')
        .getValue(DurationPage.durationMonths()).should.eventually.contain('')
        .isSelected(DurationPage.durationExclusiveIPreferNotToSay()).should('be.false')

        // When
        .get(DurationPage.submit()).click()

        // Then
        .get(SummaryPage.durationAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
