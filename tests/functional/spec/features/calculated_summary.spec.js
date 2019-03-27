const helpers = require('../../helpers');

const FirstNumberBlockPage = require('../../generated_pages/calculated_summary/first-number-block.page.js');
const SecondNumberBlockPage = require('../../generated_pages/calculated_summary/second-number-block.page.js');
const ThirdNumberBlockPage = require('../../generated_pages/calculated_summary/third-number-block.page.js');
const ThirdAndAHalfNumberBlockPage = require('../../generated_pages/calculated_summary/third-and-a-half-number-block.page.js');
const SkipFourthBlockPage = require('../../generated_pages/calculated_summary/skip-fourth-block.page.js');
const FourthNumberBlockPage = require('../../generated_pages/calculated_summary/fourth-number-block.page.js');
const FourthAndAHalfNumberBlockPage = require('../../generated_pages/calculated_summary/fourth-and-a-half-number-block.page.js');
const FifthNumberBlockPage = require('../../generated_pages/calculated_summary/fifth-number-block.page.js');
const SixthNumberBlockPage = require('../../generated_pages/calculated_summary/sixth-number-block.page.js');
const CurrencyTotalPlaybackPageWithFourth = require('../../generated_pages/calculated_summary/currency-total-playback-with-fourth.page.js');
const CurrencyTotalPlaybackPageSkippedFourth = require('../../generated_pages/calculated_summary/currency-total-playback-skipped-fourth.page.js');
const UnitTotalPlaybackPage = require('../../generated_pages/calculated_summary/unit-total-playback.page.js');
const PercentageTotalPlaybackPage = require('../../generated_pages/calculated_summary/percentage-total-playback.page.js');
const NumberTotalPlaybackPage = require('../../generated_pages/calculated_summary/number-total-playback.page.js');
const SummaryPage = require('../../base_pages/summary.page.js');
const ThankYouPage = require('../../base_pages/thank-you.page.js');

describe('Feature: Calculated Summary', function() {

  describe('Given I have a Calculated Summary', function() {

    before('Get to Calculated Summary', function () {
      return helpers.openQuestionnaire('test_calculated_summary.json').then(() => {
        return browser
          .setValue(FirstNumberBlockPage.firstNumber(), 1.23)
        .click(FirstNumberBlockPage.submit())

        .setValue(SecondNumberBlockPage.secondNumber(), 4.56)
        .setValue(SecondNumberBlockPage.secondNumberUnitTotal(), 789)
        .setValue(SecondNumberBlockPage.secondNumberAlsoInTotal(), 0.12)
        .click(SecondNumberBlockPage.submit())

        .setValue(ThirdNumberBlockPage.thirdNumber(), 3.45)
        .click(ThirdNumberBlockPage.submit())
        .setValue(ThirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal(), 678)
        .click(ThirdAndAHalfNumberBlockPage.submit())

        .click(SkipFourthBlockPage.no())
        .click(SkipFourthBlockPage.submit())

        .setValue(FourthNumberBlockPage.fourthNumber(), 9.01)
        .click(FourthNumberBlockPage.submit())
        .setValue(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal(), 2.34)
        .click(FourthAndAHalfNumberBlockPage.submit())

        .setValue(FifthNumberBlockPage.fifthPercent(), 56)
        .setValue(FifthNumberBlockPage.fifthNumber(), 78.91)
        .click(FifthNumberBlockPage.submit())

        .setValue(SixthNumberBlockPage.sixthPercent(), 23)
        .setValue(SixthNumberBlockPage.sixthNumber(), 45.67)
        .click(SixthNumberBlockPage.submit())

        .getUrl().should.eventually.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
      });
    });

  it('Given I complete every question, When i get to the currency summary, Then I should see the correct total', function() {
    return browser
      // Totals and titles should be shown
      .getText(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).should.eventually.contain('We calculate the total of currency values entered to be £20.71. Is this correct?')
      .getText(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryQuestion()).should.eventually.contain('Grand total of previous values')
      .getText(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).should.eventually.contain('£20.71')

      // Answers included in calculation should be shown
      .getText(CurrencyTotalPlaybackPageWithFourth.firstNumberAnswerLabel()).should.eventually.contain('First answer label')
      .getText(CurrencyTotalPlaybackPageWithFourth.firstNumberAnswer()).should.eventually.contain('£1.23')
      .getText(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerLabel()).should.eventually.contain('Second answer in currency label')
      .getText(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswer()).should.eventually.contain('£4.56')
      .getText(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerAlsoInTotalLabel()).should.eventually.contain('Second answer label also in currency total (optional)')
      .getText(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerAlsoInTotal()).should.eventually.contain('£0.12')
      .getText(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerLabel()).should.eventually.contain('Third answer label')
      .getText(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswer()).should.eventually.contain('£3.45')
      .getText(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerLabel()).should.eventually.contain('Fourth answer label (optional)')
      .getText(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer()).should.eventually.contain('£9.01')
      .getText(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotalLabel()).should.eventually.contain('Fourth answer label also in total (optional)')
      .getText(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal()).should.eventually.contain('£2.34')

      // Answers not included in calculation should not be shown
      .elements(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).then(result => result.value).should.eventually.be.empty
      .elements(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).then(result => result.value).should.eventually.be.empty
      .elements(NumberTotalPlaybackPage.fifthNumberAnswer()).then(result => result.value).should.eventually.be.empty
      .elements(NumberTotalPlaybackPage.sixthNumberAnswer()).then(result => result.value).should.eventually.be.empty;
    });

    it('Given change an answer, When i get to the currency summary, Then I should see the new total', function() {
      return browser
        .click(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerEdit())
        .setValue(FourthNumberBlockPage.fourthNumber(), 19.01)
        .click(FourthNumberBlockPage.submit())
        .setValue(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal(), 12.34)
        .click(FourthAndAHalfNumberBlockPage.submit())

        .click(FifthNumberBlockPage.submit())
        .click(SixthNumberBlockPage.submit())

        .getUrl().should.eventually.contain(CurrencyTotalPlaybackPageWithFourth.pageName)
        .getText(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).should.eventually.contain('We calculate the total of currency values entered to be £40.71. Is this correct?')
        .getText(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).should.eventually.contain('£40.71');
    });

    it('Given I leave an answer empty, When i get to the currency summary, Then I should see no answer provided and new total', function() {
      return browser
        .click(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerEdit())
        .setValue(FourthNumberBlockPage.fourthNumber(), '')
        .click(FourthNumberBlockPage.submit())
        .setValue(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal(), '')
        .click(FourthAndAHalfNumberBlockPage.submit())

        .click(FifthNumberBlockPage.submit())
        .click(SixthNumberBlockPage.submit())

        .getUrl().should.eventually.contain(CurrencyTotalPlaybackPageWithFourth.pageName)
        .getText(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).should.eventually.contain('We calculate the total of currency values entered to be £9.36. Is this correct?')
        .getText(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).should.eventually.contain('£9.36')
        .getText(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer()).should.eventually.contain('No answer provided');
    });


    it('Given I skip the fourth page, When i get to the playback, Then I can should not see it in the total', function() {
      return browser
        .click(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerEdit())
        .click(ThirdNumberBlockPage.submit())
        .click(ThirdAndAHalfNumberBlockPage.submit())

        .click(SkipFourthBlockPage.yes())
        .click(SkipFourthBlockPage.submit())

        .click(FifthNumberBlockPage.submit())
        .click(SixthNumberBlockPage.submit())

        .getUrl().should.eventually.contain(CurrencyTotalPlaybackPageSkippedFourth.pageName)
        .elements(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer()).then(result => result.value).should.eventually.be.empty
        .elements(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal()).then(result => result.value).should.eventually.be.empty
        .getText(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).should.eventually.contain('We calculate the total of currency values entered to be £9.36. Is this correct?')
        .getText(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryAnswer()).should.eventually.contain('£9.36');

    });

    it('Given I complete every question, When i get to the unit summary, Then I should see the correct total', function() {
      return browser
        // Totals and titles should be shown
        .click(CurrencyTotalPlaybackPageWithFourth.submit())
        .getText(UnitTotalPlaybackPage.calculatedSummaryTitle()).should.eventually.contain('We calculate the total of unit values entered to be 1,467 cm. Is this correct?')
        .getText(UnitTotalPlaybackPage.calculatedSummaryQuestion()).should.eventually.contain('Grand total of previous values')
        .getText(UnitTotalPlaybackPage.calculatedSummaryAnswer()).should.eventually.contain('1,467 cm')

        // Answers included in calculation should be shown
        .getText(UnitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).should.eventually.contain('Second answer label in unit total')
        .getText(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).should.eventually.contain('789 cm')
        .getText(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotalLabel()).should.eventually.contain('Third answer label in unit total')
        .getText(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).should.eventually.contain('678 cm');
    });

    it('Given I complete every question, When i get to the percentage summary, Then I should see the correct total', function() {
      return browser
        // Totals and titles should be shown
        .click(UnitTotalPlaybackPage.submit())
        .getText(UnitTotalPlaybackPage.calculatedSummaryTitle()).should.eventually.contain('We calculate the total of percentage values entered to be 79%. Is this correct?')
        .getText(UnitTotalPlaybackPage.calculatedSummaryQuestion()).should.eventually.contain('Grand total of previous values')
        .getText(UnitTotalPlaybackPage.calculatedSummaryAnswer()).should.eventually.contain('79%')

        // Answers included in calculation should be shown
        .getText(PercentageTotalPlaybackPage.fifthPercentAnswerLabel()).should.eventually.contain('Fifth answer label percentage tota')
        .getText(PercentageTotalPlaybackPage.fifthPercentAnswer()).should.eventually.contain('56%')
        .getText(PercentageTotalPlaybackPage.sixthPercentAnswerLabel()).should.eventually.contain('Sixth answer label percentage tota')
        .getText(PercentageTotalPlaybackPage.sixthPercentAnswer()).should.eventually.contain('23%');
    });

    it('Given I complete every question, When i get to the number summary, Then I should see the correct total', function() {
      return browser
        // Totals and titles should be shown
        .click(UnitTotalPlaybackPage.submit())
        .getText(UnitTotalPlaybackPage.calculatedSummaryTitle()).should.eventually.contain('We calculate the total of number values entered to be 124.58. Is this correct?')
        .getText(UnitTotalPlaybackPage.calculatedSummaryQuestion()).should.eventually.contain('Grand total of previous values')
        .getText(UnitTotalPlaybackPage.calculatedSummaryAnswer()).should.eventually.contain('124.58')

        // Answers included in calculation should be shown
        .getText(NumberTotalPlaybackPage.fifthNumberAnswerLabel()).should.eventually.contain('Fifth answer label number total')
        .getText(NumberTotalPlaybackPage.fifthNumberAnswer()).should.eventually.contain('78.91')
        .getText(NumberTotalPlaybackPage.sixthNumberAnswerLabel()).should.eventually.contain('Sixth answer label number total')
        .getText(NumberTotalPlaybackPage.sixthNumberAnswer()).should.eventually.contain('45.67');
    });

    it('Given I confirm the total, When i get to the summary, Then I can complete the survey', function() {
      return browser
        .click(NumberTotalPlaybackPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .click(SummaryPage.submit())
        .getUrl().should.eventually.contain(ThankYouPage.pageName);
    });

  });
});
