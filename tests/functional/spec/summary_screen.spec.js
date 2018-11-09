const helpers = require('../helpers');

const RadioPage = require('../generated_pages/summary/radio.page.js');
const TestNumberPage = require('../generated_pages/summary/test-number-block.page.js');
const DessertBlockPage = require('../generated_pages/summary/dessert-block.page.js');
const SummaryPage = require('../generated_pages/summary/summary.page.js');

describe('Summary Screen', function() {

  it('Given a survey has been completed when a summary page is displayed then it should contain all answers', function() {
  return helpers.openQuestionnaire('test_summary.json')
    .then(completeAllQuestions)
    .then(() => {
      return browser
        .getText(SummaryPage.radioAnswer()).should.eventually.contain('Bacon')
        .getText(SummaryPage.testCurrency()).should.eventually.contain('£1,234.00')
        .getText(SummaryPage.squareKilometres()).should.eventually.contain('123,456 km²')
        .getText(SummaryPage.testDecimal()).should.eventually.contain('123,456.78')
        .getText(SummaryPage.dessertGroupTitle()).should.eventually.contain('Dessert')
        .elements(SummaryPage.summaryGroupTitle()).then(result => result.value).should.eventually.be.empty;
      });
  });

  it('Given a survey has been completed when a summary page is displayed then I should be able to submit the answers', function() {
  return helpers.openQuestionnaire('test_summary.json')
    .then(completeAllQuestions)
    .then(() => {
      return browser
        .click(SummaryPage.submit())
        .getUrl().should.eventually.contain('thank-you');
      });
  });

  it('Given a survey has been completed when a summary page edit link is clicked then it should return to that question', function() {
  return helpers.openQuestionnaire('test_summary.json')
    .then(completeAllQuestions)
    .then(() => {
      return browser
        .click(SummaryPage.radioAnswerEdit())
        .hasFocus(RadioPage.bacon());
      });
  });

  it('Given a survey has been completed when a summary page edit link is clicked then it should return to that question then back to summary', function() {
  return helpers.openQuestionnaire('test_summary.json')
    .then(completeAllQuestions)
    .then(() => {
      return browser
        .click(SummaryPage.radioAnswerEdit())
        .click(RadioPage.sausage())
        .click(RadioPage.submit())
        .getText(SummaryPage.radioAnswer()).should.eventually.contain('Sausage');
      });
  });

  it('Given the edit link is used when a question is updated then the summary screen should show the new answer', function() {
  return helpers.openQuestionnaire('test_summary.json')
    .then(completeAllQuestions)
    .then(() => {
      return browser
        .getText(SummaryPage.squareKilometres()).should.eventually.contain('123,456 km²')
        .click(SummaryPage.squareKilometresEdit())
        .hasFocus(TestNumberPage.squareKilometres())
        .setValue(TestNumberPage.squareKilometres(), '654321')
        .click(TestNumberPage.submit())
        .getText(SummaryPage.squareKilometres()).should.eventually.contain('654,321 km²');
      });
  });

  it('Given a number value of zero is entered when on the summary screen then formatted 0 should be displayed', function() {
  return helpers.openQuestionnaire('test_summary.json').then(() => {
    return browser
      .click(RadioPage.submit())
      .setValue(TestNumberPage.testCurrency(), '0')
      .click(TestNumberPage.submit())
      .click(DessertBlockPage.submit())
      .getUrl().should.eventually.contain(SummaryPage.pageName)
      .getText(SummaryPage.testCurrency()).should.eventually.contain('£0.00');
     });
  });

  it('Given no value is entered when on the summary screen then the correct response should be displayed', function() {
  return helpers.openQuestionnaire('test_summary.json').then(() => {
    return browser
      .click(RadioPage.submit())
      .click(TestNumberPage.submit())
      .click(DessertBlockPage.submit())
      .getUrl().should.eventually.contain(SummaryPage.pageName)
      .getText(SummaryPage.testCurrency()).should.eventually.contain('No answer provided');
     });
  });


  function completeAllQuestions() {
    return browser
      .click(RadioPage.bacon())
      .click(RadioPage.submit())
      .setValue(TestNumberPage.testCurrency(), '1234')
      .setValue(TestNumberPage.squareKilometres(), '123456')
      .setValue(TestNumberPage.testDecimal(), '123456.78')
      .click(TestNumberPage.submit())
      .setValue(DessertBlockPage.dessert(), 'Crème Brûlée')
      .click(DessertBlockPage.submit())
      .getUrl().should.eventually.contain(SummaryPage.pageName);
  }

});

