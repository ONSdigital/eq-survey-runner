import {openQuestionnaire} from ../../helpers/helpers.js

const FirstNumberBlockPage = require('../../generated_pages/calculated_summary/first-number-block.page.js');
const SecondNumberBlockPage = require('../../generated_pages/calculated_summary/second-number-block.page.js');
const ThirdNumberBlockPage = require('../../generated_pages/calculated_summary/third-number-block.page.js');
const SkipFourthBlockPage = require('../../generated_pages/calculated_summary/skip-fourth-block.page.js');
const FourthNumberBlockPage = require('../../generated_pages/calculated_summary/fourth-number-block.page.js');
const FifthNumberBlockPage = require('../../generated_pages/calculated_summary/fifth-number-block.page.js');
const SixthNumberBlockPage = require('../../generated_pages/calculated_summary/sixth-number-block.page.js');
const CurrencyTotalPlaybackPage = require('../../generated_pages/calculated_summary/currency-total-playback.page.js');
const UnitTotalPlaybackPage = require('../../generated_pages/calculated_summary/unit-total-playback.page.js');
const PercentageTotalPlaybackPage = require('../../generated_pages/calculated_summary/percentage-total-playback.page.js');
const NumberTotalPlaybackPage = require('../../generated_pages/calculated_summary/number-total-playback.page.js');
const SummaryPage = require('../../base_pages/summary.page.js');
const ThankYouPage = require('../../base_pages/thank-you.page.js');

describe('Feature: Calculated Summary', function() {

  describe('Given I have a Calculated Summary', function() {

    before('Get to Calculated Summary', function () {
      openQuestionnaire('test_calculated_summary.json')
                  .get(FirstNumberBlockPage.firstNumber()).type(1.23)
        .get(FirstNumberBlockPage.submit()).click()

        .get(SecondNumberBlockPage.secondNumber()).type(4.56)
        .get(SecondNumberBlockPage.secondNumberUnitTotal()).type(789)
        .get(SecondNumberBlockPage.secondNumberAlsoInTotal()).type(0.12)
        .get(SecondNumberBlockPage.submit()).click()

        .get(ThirdNumberBlockPage.thirdNumber()).type(3.45)
        .get(ThirdNumberBlockPage.thirdNumberUnitTotal()).type(678)
        .get(ThirdNumberBlockPage.submit()).click()

        .get(SkipFourthBlockPage.no()).click()
        .get(SkipFourthBlockPage.submit()).click()

        .get(FourthNumberBlockPage.fourthNumber()).type(9.01)
        .get(FourthNumberBlockPage.fourthNumberAlsoInTotal()).type(2.34)
        .get(FourthNumberBlockPage.submit()).click()

        .get(FifthNumberBlockPage.fifthPercent()).type(56)
        .get(FifthNumberBlockPage.fifthNumber()).type(78.91)
        .get(FifthNumberBlockPage.submit()).click()

        .get(SixthNumberBlockPage.sixthPercent()).type(23)
        .get(SixthNumberBlockPage.sixthNumber()).type(45.67)
        .get(SixthNumberBlockPage.submit()).click()

        .url().should('contain', CurrencyTotalPlaybackPage.pageName);
      });
    });

  it('Given I complete every question, When i get to the currency summary, Then I should see the correct total', function() {
          // Totals and titles should be shown
      .get(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).stripText().should('contain', 'We calculate the total of currency values entered to be £20.71. Is this correct?')
      .get(CurrencyTotalPlaybackPage.calculatedSummaryQuestion()).stripText().should('contain', 'Grand total of previous values')
      .get(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).stripText().should('contain', '£20.71')

      // Answers included in calculation should be shown
      .get(CurrencyTotalPlaybackPage.firstNumberAnswerLabel()).stripText().should('contain', 'First answer label')
      .get(CurrencyTotalPlaybackPage.firstNumberAnswer()).stripText().should('contain', '£1.23')
      .get(CurrencyTotalPlaybackPage.secondNumberAnswerLabel()).stripText().should('contain', 'Second answer in currency label')
      .get(CurrencyTotalPlaybackPage.secondNumberAnswer()).stripText().should('contain', '£4.56')
      .get(CurrencyTotalPlaybackPage.secondNumberAnswerAlsoInTotalLabel()).stripText().should('contain('Second answer label also in currency total ', optional)')
      .get(CurrencyTotalPlaybackPage.secondNumberAnswerAlsoInTotal()).stripText().should('contain', '£0.12')
      .get(CurrencyTotalPlaybackPage.thirdNumberAnswerLabel()).stripText().should('contain', 'Third answer label')
      .get(CurrencyTotalPlaybackPage.thirdNumberAnswer()).stripText().should('contain', '£3.45')
      .get(CurrencyTotalPlaybackPage.fourthNumberAnswerLabel()).stripText().should('contain('Fourth answer label ', optional)')
      .get(CurrencyTotalPlaybackPage.fourthNumberAnswer()).stripText().should('contain', '£9.01')
      .get(CurrencyTotalPlaybackPage.fourthNumberAnswerAlsoInTotalLabel()).stripText().should('contain('Fourth answer label also in total ', optional)')
      .get(CurrencyTotalPlaybackPage.fourthNumberAnswerAlsoInTotal()).stripText().should('contain', '£2.34')

      // Answers not included in calculation should not be shown
      .elements(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).then(result => result.value).should.eventually.be.empty
      .elements(UnitTotalPlaybackPage.thirdNumberAnswerUnitTotal()).then(result => result.value).should.eventually.be.empty
      .elements(NumberTotalPlaybackPage.fifthNumberAnswer()).then(result => result.value).should.eventually.be.empty
      .elements(NumberTotalPlaybackPage.sixthNumberAnswer()).then(result => result.value).should.eventually.be.empty;
    });

    it('Given change an answer, When i get to the currency summary, Then I should see the new total', function() {
              .get(CurrencyTotalPlaybackPage.fourthNumberAnswerEdit()).click()
        .get(FourthNumberBlockPage.fourthNumber()).type(19.01)
        .get(FourthNumberBlockPage.fourthNumberAlsoInTotal()).type(12.34)
        .get(FourthNumberBlockPage.submit()).click()

        .get(FifthNumberBlockPage.submit()).click()
        .get(SixthNumberBlockPage.submit()).click()

        .url().should('contain', CurrencyTotalPlaybackPage.pageName)
        .get(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).stripText().should('contain', 'We calculate the total of currency values entered to be £40.71. Is this correct?')
        .get(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).stripText().should('contain', '£40.71');
    });

    it('Given I leave an answer empty, When i get to the currency summary, Then I should see no answer provided and new total', function() {
              .get(CurrencyTotalPlaybackPage.fourthNumberAnswerEdit()).click()
        .get(FourthNumberBlockPage.fourthNumber()).clear()
        .get(FourthNumberBlockPage.fourthNumberAlsoInTotal()).clear()
        .get(FourthNumberBlockPage.submit()).click()

        .get(FifthNumberBlockPage.submit()).click()
        .get(SixthNumberBlockPage.submit()).click()

        .url().should('contain', CurrencyTotalPlaybackPage.pageName)
        .get(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).stripText().should('contain', 'We calculate the total of currency values entered to be £9.36. Is this correct?')
        .get(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).stripText().should('contain', '£9.36')
        .get(CurrencyTotalPlaybackPage.fourthNumberAnswer()).stripText().should('contain', 'No answer provided');
    });


    it('Given I skip the fourth page, When i get to the playback, Then I can should not see it in the total', function() {
              .get(CurrencyTotalPlaybackPage.thirdNumberAnswerEdit()).click()
        .get(ThirdNumberBlockPage.submit()).click()

        .get(SkipFourthBlockPage.yes()).click()
        .get(SkipFourthBlockPage.submit()).click()

        .get(FifthNumberBlockPage.submit()).click()
        .get(SixthNumberBlockPage.submit()).click()

        .url().should('contain', CurrencyTotalPlaybackPage.pageName)
        .elements(CurrencyTotalPlaybackPage.fourthNumberAnswer()).then(result => result.value).should.eventually.be.empty
        .elements(CurrencyTotalPlaybackPage.fourthNumberAnswerAlsoInTotal()).then(result => result.value).should.eventually.be.empty
        .get(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).stripText().should('contain', 'We calculate the total of currency values entered to be £9.36. Is this correct?')
        .get(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).stripText().should('contain', '£9.36');

    });

    it('Given I complete every question, When i get to the unit summary, Then I should see the correct total', function() {
              // Totals and titles should be shown
        .get(CurrencyTotalPlaybackPage.submit()).click()
        .get(UnitTotalPlaybackPage.calculatedSummaryTitle()).stripText().should('contain', 'We calculate the total of unit values entered to be 1,467 cm. Is this correct?')
        .get(UnitTotalPlaybackPage.calculatedSummaryQuestion()).stripText().should('contain', 'Grand total of previous values')
        .get(UnitTotalPlaybackPage.calculatedSummaryAnswer()).stripText().should('contain', '1,467 cm')

        // Answers included in calculation should be shown
        .get(UnitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).stripText().should('contain', 'Second answer label in unit total')
        .get(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).stripText().should('contain', '789 cm')
        .get(UnitTotalPlaybackPage.thirdNumberAnswerUnitTotalLabel()).stripText().should('contain', 'Third answer label in unit total')
        .get(UnitTotalPlaybackPage.thirdNumberAnswerUnitTotal()).stripText().should('contain', '678 cm');
    });

    it('Given I complete every question, When i get to the percentage summary, Then I should see the correct total', function() {
              // Totals and titles should be shown
        .get(UnitTotalPlaybackPage.submit()).click()
        .get(UnitTotalPlaybackPage.calculatedSummaryTitle()).stripText().should('contain', 'We calculate the total of percentage values entered to be 79%. Is this correct?')
        .get(UnitTotalPlaybackPage.calculatedSummaryQuestion()).stripText().should('contain', 'Grand total of previous values')
        .get(UnitTotalPlaybackPage.calculatedSummaryAnswer()).stripText().should('contain', '79%')

        // Answers included in calculation should be shown
        .get(PercentageTotalPlaybackPage.fifthPercentAnswerLabel()).stripText().should('contain', 'Fifth answer label percentage tota')
        .get(PercentageTotalPlaybackPage.fifthPercentAnswer()).stripText().should('contain', '56%')
        .get(PercentageTotalPlaybackPage.sixthPercentAnswerLabel()).stripText().should('contain', 'Sixth answer label percentage tota')
        .get(PercentageTotalPlaybackPage.sixthPercentAnswer()).stripText().should('contain', '23%');
    });

    it('Given I complete every question, When i get to the number summary, Then I should see the correct total', function() {
              // Totals and titles should be shown
        .get(UnitTotalPlaybackPage.submit()).click()
        .get(UnitTotalPlaybackPage.calculatedSummaryTitle()).stripText().should('contain', 'We calculate the total of number values entered to be 124.58. Is this correct?')
        .get(UnitTotalPlaybackPage.calculatedSummaryQuestion()).stripText().should('contain', 'Grand total of previous values')
        .get(UnitTotalPlaybackPage.calculatedSummaryAnswer()).stripText().should('contain', '124.58')

        // Answers included in calculation should be shown
        .get(NumberTotalPlaybackPage.fifthNumberAnswerLabel()).stripText().should('contain', 'Fifth answer label number total')
        .get(NumberTotalPlaybackPage.fifthNumberAnswer()).stripText().should('contain', '78.91')
        .get(NumberTotalPlaybackPage.sixthNumberAnswerLabel()).stripText().should('contain', 'Sixth answer label number total')
        .get(NumberTotalPlaybackPage.sixthNumberAnswer()).stripText().should('contain', '45.67');
    });

    it('Given I confirm the total, When i get to the summary, Then I can complete the survey', function() {
              .get(NumberTotalPlaybackPage.submit()).click()
        .url().should('contain', SummaryPage.pageName)
        .get(SummaryPage.submit()).click()
        .url().should('contain', ThankYouPage.pageName);
    });

  });
});
