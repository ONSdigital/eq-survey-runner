import {openQuestionnaire} from ../../../../helpers/helpers.js

const MonthYearDatePage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-month-year-date.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-month-year-section-summary.page');

describe('Component: Mutually Exclusive Month Year Date With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
          return browser.get(helpers.navigationLink('Month Year Date')).click();
        });
  });

  describe('Given the user has entered a value for the non-exclusive month year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

              // Given
        .get(MonthYearDatePage.monthYearDateMonth()).select(3)
        .get(MonthYearDatePage.monthYearDateYear()).type('2018')
        .get(MonthYearDatePage.monthYearDateMonth()).stripText().should('contain', 'March')
        .get(MonthYearDatePage.monthYearDateYear()).invoke('val').should('contain', '2018')

        // When
        .get(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click()

        // Then
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should('be.true')
        .get(MonthYearDatePage.monthYearDateMonth()).invoke('val').should('contain', '')
        .get(MonthYearDatePage.monthYearDateYear()).invoke('val').should('contain', '')

        .get(MonthYearDatePage.submit()).click()

        .get(SummaryPage.monthYearDateExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.monthYearDateExclusiveAnswer()).should('not.have.string', 'March 2018');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', function() {

              // Given
        .get(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click()
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should('be.true')

        // When
        .get(MonthYearDatePage.monthYearDateMonth()).select(3)
        .get(MonthYearDatePage.monthYearDateYear()).type('2018')

        // Then
        .get(MonthYearDatePage.monthYearDateMonth()).stripText().should('contain', 'March')
        .get(MonthYearDatePage.monthYearDateYear()).invoke('val').should('contain', '2018')

        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should('be.false')

        .get(MonthYearDatePage.submit()).click()

        .get(SummaryPage.monthYearDateAnswer()).stripText().should('have.string', 'March 2018')
        .get(SummaryPage.monthYearDateAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', function() {

              // Given
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should('be.false')

        // When
        .get(MonthYearDatePage.monthYearDateMonth()).select(3)
        .get(MonthYearDatePage.monthYearDateYear()).type('2018')

        // Then
        .get(MonthYearDatePage.monthYearDateMonth()).stripText().should('contain', 'March')
        .get(MonthYearDatePage.monthYearDateYear()).invoke('val').should('contain', '2018')
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should('be.false')

        .get(MonthYearDatePage.submit()).click()

        .get(SummaryPage.monthYearDateAnswer()).stripText().should('have.string', 'March 2018')
        .get(SummaryPage.monthYearDateAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive month year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

              // Given
        .get(MonthYearDatePage.monthYearDateMonth()).invoke('val').should('contain', '')
        .get(MonthYearDatePage.monthYearDateYear()).invoke('val').should('contain', '')

        // When
        .get(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click()
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should('be.true')

        // Then
        .get(MonthYearDatePage.submit()).click()

        .get(SummaryPage.monthYearDateExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.monthYearDateExclusiveAnswer()).should('not.have.string', 'March 2018');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

              // Given
        .get(MonthYearDatePage.monthYearDateMonth()).invoke('val').should('contain', '')
        .get(MonthYearDatePage.monthYearDateYear()).invoke('val').should('contain', '')
        .isSelected(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).should('be.false')

        // When
        .get(MonthYearDatePage.submit()).click()

        // Then
        .get(SummaryPage.monthYearDateAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
