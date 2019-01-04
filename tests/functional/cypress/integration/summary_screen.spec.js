import {openQuestionnaire} from '../helpers/helpers.js';

const RadioPage = require('../../generated_pages/summary/radio.page.js');
const TestNumberPage = require('../../generated_pages/summary/test-number-block.page.js');
const DessertBlockPage = require('../../generated_pages/summary/dessert-block.page.js');
const SummaryPage = require('../../generated_pages/summary/summary.page.js');

describe('Summary Screen', function() {

  beforeEach(() => {
    openQuestionnaire('test_summary.json');
  });

  it('Given a survey has been completed when a summary page is displayed then it should contain all answers', function() {
    completeAllQuestions();
    cy
      .get(SummaryPage.radioAnswer()).stripText().should('contain', 'Bacon')
      .get(SummaryPage.testCurrency()).stripText().should('contain', '£1,234.00')
      .get(SummaryPage.squareKilometres()).stripText().should('contain', '123,456 km²')
      .get(SummaryPage.testDecimal()).stripText().should('contain', '123,456.78')
      .get(SummaryPage.dessertGroupTitle()).stripText().should('contain', 'Dessert')
      .get(SummaryPage.summaryGroupTitle()).should('not.exist');
  });

  it('Given a survey has been completed when a summary page is displayed then I should be able to submit the answers', function() {
    completeAllQuestions();
    cy
      .get(SummaryPage.submit()).click()
      .url().should('contain', 'thank-you');
  });

  it('Given a survey has been completed when a summary page edit link is clicked then it should return to that question', function() {
    completeAllQuestions();
    cy
      .get(SummaryPage.radioAnswerEdit()).click()
      .get(RadioPage.bacon()).should('be.checked');
  });

  it('Given a survey has been completed when a summary page edit link is clicked then it should return to that question then back to summary', function() {
    completeAllQuestions();
    cy
      .get(SummaryPage.radioAnswerEdit()).click()
      .get(RadioPage.sausage()).click()
      .get(RadioPage.submit()).click()
      .get(SummaryPage.radioAnswer()).stripText().should('contain', 'Sausage');
  });

  it('Given the edit link is used when a question is updated then the summary screen should show the new answer', function() {
    completeAllQuestions();
    cy
      .get(SummaryPage.squareKilometres()).stripText().should('contain', '123,456 km²')
      .get(SummaryPage.squareKilometresEdit()).click()
      //.focused().should('match', TestNumberPage.squareKilometres())
      .get(TestNumberPage.squareKilometres()).clear().type('654321')
      .get(TestNumberPage.submit()).click()
      .get(SummaryPage.squareKilometres()).stripText().should('contain', '654,321 km²');
  });

  it('Given a number value of zero is entered when on the summary screen then formatted 0 should be displayed', function() {
    cy
      .get(RadioPage.submit()).click()
      .get(TestNumberPage.testCurrency()).type('0')
      .get(TestNumberPage.submit()).click()
      .get(DessertBlockPage.submit()).click()
      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.testCurrency()).stripText().should('contain', '£0.00');
  });

  it('Given no value is entered when on the summary screen then the correct response should be displayed', function() {
    cy
      .get(RadioPage.submit()).click()
      .get(TestNumberPage.submit()).click()
      .get(DessertBlockPage.submit()).click()
      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.testCurrency()).stripText().should('contain', 'No answer provided');
  });
});

function completeAllQuestions() {
  cy
    .get(RadioPage.bacon()).click()
    .get(RadioPage.submit()).click()
    .get(TestNumberPage.testCurrency()).type('1234')
    .get(TestNumberPage.squareKilometres()).type('123456')
    .get(TestNumberPage.testDecimal()).type('123456.78')
    .get(TestNumberPage.submit()).click()
    .get(DessertBlockPage.dessert()).type('Crème Brûlée')
    .get(DessertBlockPage.submit()).click()
    .url().should('contain', SummaryPage.pageName);
}
