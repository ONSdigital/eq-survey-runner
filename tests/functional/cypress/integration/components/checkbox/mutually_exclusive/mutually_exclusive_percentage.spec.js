import {openQuestionnaire} from ../../../../helpers/helpers.js

const PercentagePage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-percentage.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-percentage-section-summary.page');

describe('Component: Mutually Exclusive Percentage With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
          return browser.get(helpers.navigationLink('Percentage')).click();
        });
  });

  describe('Given the user has entered a value for the non-exclusive percentage answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

              // Given
        .get(PercentagePage.percentage()).type('99')
        .getValue(PercentagePage.percentage()).should.eventually.contain('99')

        // When
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).click()

        // Then
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(PercentagePage.percentage()).should.eventually.contain('')

        .get(PercentagePage.submit()).click()

        .get(SummaryPage.percentageExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.percentageExclusiveAnswer()).should('not.have.string', '99');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive percentage answer and removes focus, Then only the non-exclusive percentage answer should be answered.', function() {

              // Given
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).click()
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .get(PercentagePage.percentage()).type('99')

        // Then
        .getValue(PercentagePage.percentage()).should.eventually.contain('99')
        .get(PercentagePage.percentageLabel()).click()
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.false

        .get(PercentagePage.submit()).click()

        .get(SummaryPage.percentageAnswer()).stripText().should('have.string', '99')
        .get(SummaryPage.percentageAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive percentage answer, Then only the non-exclusive percentage answer should be answered.', function() {

              // Given
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .get(PercentagePage.percentage()).type('99')

        // Then
        .getValue(PercentagePage.percentage()).should.eventually.contain('99')
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.false

        .get(PercentagePage.submit()).click()

        .get(SummaryPage.percentageAnswer()).stripText().should('have.string', '99')
        .get(SummaryPage.percentageAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive percentage answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

              // Given
        .getValue(PercentagePage.percentage()).should.eventually.contain('')

        // When
        .get(PercentagePage.percentageExclusiveIPreferNotToSay()).click()
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .get(PercentagePage.submit()).click()

        .get(SummaryPage.percentageExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.percentageExclusiveAnswer()).should('not.have.string', 'British\nIrish');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

              // Given
        .getValue(PercentagePage.percentage()).should.eventually.contain('')
        .isSelected(PercentagePage.percentageExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .get(PercentagePage.submit()).click()

        // Then
        .get(SummaryPage.percentageAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
