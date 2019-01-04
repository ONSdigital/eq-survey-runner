import {openQuestionnaire} from '../helpers/helpers.js';

const TestErrorsPage = require('../../generated_pages/error_messages/test-errors.page.js');

describe('Error Messages', function() {

  beforeEach(() => {
    openQuestionnaire('test_error_messages.json');
  });

  it('Given a survey has an error when errors are displayed then page error messages are correct', function() {
    cy
      .get(TestErrorsPage.testNumber()).type('cat')
      .get(TestErrorsPage.testPercent()).type('101')
      .get(TestErrorsPage.testCurrency()).type('123.456')
      .get(TestErrorsPage.submit()).click()
      .get(TestErrorsPage.errorHeader()).stripText().should('contain', 'This page has 3 errors')
      .get(TestErrorsPage.errorNumber(1)).stripText().should('contain', 'Enter a number.')
      .get(TestErrorsPage.errorNumber(2)).stripText().should('contain', 'Enter an answer less than or equal to 100.')
      .get(TestErrorsPage.errorNumber(3)).stripText().should('contain', 'Enter a number rounded to 2 decimal places.');
  });

  it('Given a survey has 1 error when error is displayed then error header is displayed correct', function() {
    cy
      .get(TestErrorsPage.testNumber()).type('cat')
      .get(TestErrorsPage.testPercent()).type('100')
      .get(TestErrorsPage.testCurrency()).type('123.45')
      .get(TestErrorsPage.submit()).click()
      .get(TestErrorsPage.errorHeader()).stripText().should('contain', 'This page has an error');
  });

  it('Given a survey has an error when errors are displayed then answer error messages are correct', function() {
    cy
      .get(TestErrorsPage.testNumber()).type('cat')
      .get(TestErrorsPage.testPercent()).type('101')
      .get(TestErrorsPage.testCurrency()).type('123.456')
      .get(TestErrorsPage.submit()).click()

      .get(TestErrorsPage.testNumberErrorItem()).stripText().should('contain', 'Enter a number.')
      .get(TestErrorsPage.testPercentErrorItem()).stripText().should('contain', 'Enter an answer less than or equal to 100.')
      .get(TestErrorsPage.testCurrencyErrorItem()).stripText().should('contain', 'Enter a number rounded to 2 decimal places.');
  });


  it('Given a survey has an error when errors message is clicked then the correct answer is focused', function() {
    cy
      .get(TestErrorsPage.testNumber()).type('cat')
      .get(TestErrorsPage.testPercent()).type('101')
      .get(TestErrorsPage.testCurrency()).type('123.456')
      .get(TestErrorsPage.submit()).click()

      .get(TestErrorsPage.errorNumber(2)).click()
      .focused().should('match', TestErrorsPage.testPercent())
      .get(TestErrorsPage.errorNumber(3)).click()
      .focused().should('match', TestErrorsPage.testCurrency())
      .get(TestErrorsPage.errorNumber(1)).click()
      .focused().should('match', TestErrorsPage.testNumber());
  });

});

