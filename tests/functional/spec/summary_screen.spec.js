const helpers = require('../helpers');

const RadioPage = require('../generated_pages/summary/radio.page.js');
const TestNumberPage = require('../generated_pages/summary/test-number-block.page.js');
const DessertBlockPage = require('../generated_pages/summary/dessert-block.page.js');
const SummaryPage = require('../generated_pages/summary/summary.page.js');

describe('Summary Screen', function() {
  let browser;

  beforeEach('Load the survey', function () {
    helpers.openQuestionnaire('test_summary.json').then(openBrowser => browser = openBrowser);
  });

  it('Given a survey has been completed when a summary page is displayed then it should contain all answers', function() {
    completeAllQuestions();

    expect($(SummaryPage.radioAnswer()).getText()).to.contain('Bacon');
    expect($(SummaryPage.testCurrency()).getText()).to.contain('£1,234.00');
    expect($(SummaryPage.squareKilometres()).getText()).to.contain('123,456 km²');
    expect($(SummaryPage.testDecimal()).getText()).to.contain('123,456.78');
    expect($(SummaryPage.dessertGroupTitle()).getText()).to.contain('Dessert');

    expect($$(SummaryPage.summaryGroupTitle())).to.be.empty;
  });

  it('Given a survey has been completed when a summary page is displayed then I should be able to submit the answers', function() {
    completeAllQuestions();

    $(SummaryPage.submit()).click();
    expect(browser.getUrl()).to.contain('thank-you');
  });

  it('Given a survey has been completed when a summary page edit link is clicked then it should return to that question', function() {
    completeAllQuestions();

    $(SummaryPage.radioAnswerEdit()).click();

    expect($(RadioPage.bacon()).isSelected()).to.be.true;
  });

  it('Given a survey has been completed when a summary page edit link is clicked then it should return to that question then back to summary', function() {
    completeAllQuestions();

    $(SummaryPage.radioAnswerEdit()).click();
    $(RadioPage.sausage()).click();
    $(RadioPage.submit()).click();
    expect($(SummaryPage.radioAnswer()).getText()).to.contain('Sausage');
  });

  it('Given the edit link is used when a question is updated then the summary screen should show the new answer', function() {
    completeAllQuestions();

    expect($(SummaryPage.squareKilometres()).getText()).to.contain('123,456 km²');
    $(SummaryPage.squareKilometresEdit()).click();
    expect($(TestNumberPage.squareKilometres()).isFocused()).to.be.true;
    $(TestNumberPage.squareKilometres()).setValue('654321');
    $(TestNumberPage.submit()).click();
    expect($(SummaryPage.squareKilometres()).getText()).to.contain('654,321 km²');
  });

  it('Given a number value of zero is entered when on the summary screen then formatted 0 should be displayed', function() {
    $(RadioPage.submit()).click();
    $(TestNumberPage.testCurrency()).setValue('0');
    $(TestNumberPage.submit()).click();
    $(DessertBlockPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.testCurrency()).getText()).to.contain('£0.00');
  });

  it('Given no value is entered when on the summary screen then the correct response should be displayed', function() {
    $(RadioPage.submit()).click();
    $(TestNumberPage.submit()).click();
    $(DessertBlockPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.testCurrency()).getText()).to.contain('No answer provided');
  });

  function completeAllQuestions() {
    $(RadioPage.bacon()).click();
    $(RadioPage.submit()).click();
    $(TestNumberPage.testCurrency()).setValue('1234');
    $(TestNumberPage.squareKilometres()).setValue('123456');
    $(TestNumberPage.testDecimal()).setValue('123456.78');
    $(TestNumberPage.submit()).click();
    $(DessertBlockPage.dessert()).setValue('Crème Brûlée');
    $(DessertBlockPage.submit()).click();

    let expectedUrl = browser.getUrl();

    expect(expectedUrl).to.contain(SummaryPage.pageName);
  }
});

