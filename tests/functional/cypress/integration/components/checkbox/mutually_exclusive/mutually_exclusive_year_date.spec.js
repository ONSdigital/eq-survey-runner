import {openQuestionnaire} from ../../../../helpers/helpers.js

const YearDatePage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-year-date.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-year-section-summary.page');

describe('Component: Mutually Exclusive Year Date With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
          return browser.get(helpers.navigationLink('Year Date')).click();
        });
  });

  describe('Given the user has entered a value for the non-exclusive year date answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

              // Given
        .get(YearDatePage.yearDateYear()).type('2018')
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('2018')

        // When
        .get(YearDatePage.yearDateExclusiveIPreferNotToSay()).click()

        // Then
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('')

        .get(YearDatePage.submit()).click()

        .get(SummaryPage.yearDateExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.yearDateExclusiveAnswer()).should('not.have.string', '2018');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive year date answer and removes focus, Then only the non-exclusive year date answer should be answered.', function() {

              // Given
        .get(YearDatePage.yearDateExclusiveIPreferNotToSay()).click()
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .get(YearDatePage.yearDateYear()).type('2018')

        // Then
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('2018')
        .get(YearDatePage.yearDateYearLabel()).click()
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        .get(YearDatePage.submit()).click()

        .get(SummaryPage.yearDateAnswer()).stripText().should('have.string', '2018')
        .get(SummaryPage.yearDateAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive year date answer, Then only the non-exclusive year date answer should be answered.', function() {

              // Given
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .get(YearDatePage.yearDateYear()).type('2018')

        // Then
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('2018')
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        .get(YearDatePage.submit()).click()

        .get(SummaryPage.yearDateAnswer()).stripText().should('have.string', '2018')
        .get(SummaryPage.yearDateAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive year date answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

              // Given
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('')

        // When
        .get(YearDatePage.yearDateExclusiveIPreferNotToSay()).click()
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .get(YearDatePage.submit()).click()

        .get(SummaryPage.yearDateExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.yearDateExclusiveAnswer()).should('not.have.string', '2018');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

              // Given
        .getValue(YearDatePage.yearDateYear()).should.eventually.contain('')
        .isSelected(YearDatePage.yearDateExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .get(YearDatePage.submit()).click()

        // Then
        .get(SummaryPage.yearDateAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
