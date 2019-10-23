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
  let browser;

  describe('Given I have a Calculated Summary', function() {

    before('Get to Calculated Summary', function () {
      helpers.openQuestionnaire('test_calculated_summary.json')
      .then(openBrowser => browser = openBrowser);

    $(FirstNumberBlockPage.firstNumber()).setValue(1.23);
    $(FirstNumberBlockPage.submit()).click();

    $(SecondNumberBlockPage.secondNumber()).setValue(4.56);
    $(SecondNumberBlockPage.secondNumberUnitTotal()).setValue(789);
    $(SecondNumberBlockPage.secondNumberAlsoInTotal()).setValue(0.12);
    $(SecondNumberBlockPage.submit()).click();

    $(ThirdNumberBlockPage.thirdNumber()).setValue(3.45);
    $(ThirdNumberBlockPage.submit()).click();
    $(ThirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal()).setValue(678);
    $(ThirdAndAHalfNumberBlockPage.submit()).click();

    $(SkipFourthBlockPage.no()).click();
    $(SkipFourthBlockPage.submit()).click();

    $(FourthNumberBlockPage.fourthNumber()).setValue(9.01);
    $(FourthNumberBlockPage.submit()).click();
    $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue(2.34);
    $(FourthAndAHalfNumberBlockPage.submit()).click();

    $(FifthNumberBlockPage.fifthPercent()).setValue(56);
    $(FifthNumberBlockPage.fifthNumber()).setValue(78.91);
    $(FifthNumberBlockPage.submit()).click();

    $(SixthNumberBlockPage.sixthPercent()).setValue(23);
    $(SixthNumberBlockPage.sixthNumber()).setValue(45.67);
    $(SixthNumberBlockPage.submit()).click();

    let browserUrl = browser.getUrl();

    expect(browserUrl).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
  });

  it('Given I complete every question, When i get to the currency summary, Then I should see the correct total', function() {
    // Totals and titles should be shown
    expect($(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain('We calculate the total of currency values entered to be £20.71. Is this correct?');
    expect($(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryQuestion()).getText()).to.contain('Grand total of previous values');
    expect($(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain('£20.71');

    // Answers included in calculation should be shown
    expect($(CurrencyTotalPlaybackPageWithFourth.firstNumberAnswerLabel()).getText()).to.contain('First answer label');
    expect($(CurrencyTotalPlaybackPageWithFourth.firstNumberAnswer()).getText()).to.contain('£1.23');
    expect($(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerLabel()).getText()).to.contain('Second answer in currency label');
    expect($(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswer()).getText()).to.contain('£4.56');
    expect($(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerAlsoInTotalLabel()).getText()).to.contain('Second answer label also in currency total (optional)');
    expect($(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerAlsoInTotal()).getText()).to.contain('£0.12');
    expect($(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerLabel()).getText()).to.contain('Third answer label');
    expect($(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswer()).getText()).to.contain('£3.45');
    expect($(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerLabel()).getText()).to.contain('Fourth answer label (optional)');
    expect($(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer()).getText()).to.contain('£9.01');
    expect($(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotalLabel()).getText()).to.contain('Fourth answer label also in total (optional)');
    expect($(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain('£2.34');

    // Answers not included in calculation should not be shown
    expect($$(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal())).to.be.empty;
    expect($$(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal())).to.be.empty;
    expect($$(NumberTotalPlaybackPage.fifthNumberAnswer())).to.be.empty;
    expect($$(NumberTotalPlaybackPage.sixthNumberAnswer())).to.be.empty;
  });

  it('Given change an answer, When i get to the currency summary, Then I should see the new total', function() {
      $(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerEdit()).click();
      $(FourthNumberBlockPage.fourthNumber()).setValue(19.01);
      $(FourthNumberBlockPage.submit()).click();
      $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue(12.34);
      $(FourthAndAHalfNumberBlockPage.submit()).click();

      $(FifthNumberBlockPage.submit()).click();
      $(SixthNumberBlockPage.submit()).click();

      expect(browser.getUrl()).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
      expect($(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain('We calculate the total of currency values entered to be £40.71. Is this correct?');
      expect($(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain('£40.71');
  });

  it('Given I leave an answer empty, When i get to the currency summary, Then I should see no answer provided and new total', function() {
      $(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerEdit()).click();
      $(FourthNumberBlockPage.fourthNumber()).setValue('');
      $(FourthNumberBlockPage.submit()).click();
      $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue('');
      $(FourthAndAHalfNumberBlockPage.submit()).click();

      $(FifthNumberBlockPage.submit()).click();
      $(SixthNumberBlockPage.submit()).click();

      expect(browser.getUrl()).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
      expect($(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain('We calculate the total of currency values entered to be £9.36. Is this correct?');
      expect($(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain('£9.36');
      expect($(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer()).getText()).to.contain('No answer provided');
  });


  it('Given I skip the fourth page, When i get to the playback, Then I can should not see it in the total', function() {
    $(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerEdit()).click();
    $(ThirdNumberBlockPage.submit()).click();
    $(ThirdAndAHalfNumberBlockPage.submit()).click();

    $(SkipFourthBlockPage.yes()).click();
    $(SkipFourthBlockPage.submit()).click();

    $(FifthNumberBlockPage.submit()).click();
    $(SixthNumberBlockPage.submit()).click();

    let expectedUrl = browser.getUrl();

    expect(expectedUrl).to.contain(CurrencyTotalPlaybackPageSkippedFourth.pageName);
    expect($$(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer())).to.be.empty;
    expect($$(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal())).to.be.empty;
    expect($(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain('We calculate the total of currency values entered to be £9.36. Is this correct?');
    expect($(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryAnswer()).getText()).to.contain('£9.36');
  });

  it('Given I complete every question, When i get to the unit summary, Then I should see the correct total', function() {
      // Totals and titles should be shown
      $(CurrencyTotalPlaybackPageWithFourth.submit()).click();
      expect($(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain('We calculate the total of unit values entered to be 1,467 cm. Is this correct?');
      expect($(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain('Grand total of previous values');
      expect($(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain('1,467 cm');

      // Answers included in calculation should be shown
      expect($(UnitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).getText()).to.contain('Second answer label in unit total');
      expect($(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).getText()).to.contain('789 cm');
      expect($(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotalLabel()).getText()).to.contain('Third answer label in unit total');
      expect($(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).getText()).to.contain('678 cm');
  });

  it('Given I complete every question, When i get to the percentage summary, Then I should see the correct total', function() {
      // Totals and titles should be shown
      $(UnitTotalPlaybackPage.submit()).click();
      expect($(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain('We calculate the total of percentage values entered to be 79%. Is this correct?');
      expect($(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain('Grand total of previous values');
      expect($(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain('79%');

      // Answers included in calculation should be shown
      expect($(PercentageTotalPlaybackPage.fifthPercentAnswerLabel()).getText()).to.contain('Fifth answer label percentage tota');
      expect($(PercentageTotalPlaybackPage.fifthPercentAnswer()).getText()).to.contain('56%');
      expect($(PercentageTotalPlaybackPage.sixthPercentAnswerLabel()).getText()).to.contain('Sixth answer label percentage tota');
      expect($(PercentageTotalPlaybackPage.sixthPercentAnswer()).getText()).to.contain('23%');
  });

  it('Given I complete every question, When i get to the number summary, Then I should see the correct total', function() {
      // Totals and titles should be shown
      $(UnitTotalPlaybackPage.submit()).click();
      expect($(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain('We calculate the total of number values entered to be 124.58. Is this correct?');
      expect($(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain('Grand total of previous values');
      expect($(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain('124.58');

      // Answers included in calculation should be shown
      expect($(NumberTotalPlaybackPage.fifthNumberAnswerLabel()).getText()).to.contain('Fifth answer label number total');
      expect($(NumberTotalPlaybackPage.fifthNumberAnswer()).getText()).to.contain('78.91');
      expect($(NumberTotalPlaybackPage.sixthNumberAnswerLabel()).getText()).to.contain('Sixth answer label number total');
      expect($(NumberTotalPlaybackPage.sixthNumberAnswer()).getText()).to.contain('45.67');
  });

  it('Given I confirm the total, When i get to the summary, Then I can complete the survey', function() {
      $(NumberTotalPlaybackPage.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
      $(SummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
  });

  });
});
