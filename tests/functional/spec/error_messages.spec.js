const helpers = require('../helpers');

const TestErrorsPage = require('../generated_pages/error_messages/test-errors.page.js');

describe('Error Messages', function() {

  it('Given a survey has an error when errors are displayed then page error messages are correct', function() {
    return helpers.openQuestionnaire('test_error_messages.json').then(() => {
        return browser
          .setValue(TestErrorsPage.testNumber(), 'cat')
          .setValue(TestErrorsPage.testPercent(), '101')
          .setValue(TestErrorsPage.testCurrency(), '123.456')
          .click(TestErrorsPage.submit())
          .getText(TestErrorsPage.errorHeader()).should.eventually.contain('This page has 3 errors')
          .getText(TestErrorsPage.errorNumber(1)).should.eventually.contain('Enter a number.')
          .getText(TestErrorsPage.errorNumber(2)).should.eventually.contain('Enter an answer less than or equal to 100.')
          .getText(TestErrorsPage.errorNumber(3)).should.eventually.contain('Enter a number rounded to 2 decimal places.');
    });
  });

  it('Given a survey has 1 error when error is displayed then error header is displayed correct', function() {
    return helpers.openQuestionnaire('test_error_messages.json').then(() => {
        return browser
          .setValue(TestErrorsPage.testNumber(), 'cat')
          .setValue(TestErrorsPage.testPercent(), '100')
          .setValue(TestErrorsPage.testCurrency(), '123.45')
          .click(TestErrorsPage.submit())
          .getText(TestErrorsPage.errorHeader()).should.eventually.contain('This page has an error');
    });
  });

  it('Given a survey has an error when errors are displayed then answer error messages are correct', function() {
    return helpers.openQuestionnaire('test_error_messages.json').then(() => {
        return browser
          .setValue(TestErrorsPage.testNumber(), 'cat')
          .setValue(TestErrorsPage.testPercent(), '101')
          .setValue(TestErrorsPage.testCurrency(), '123.456')
          .click(TestErrorsPage.submit())

          .getText(TestErrorsPage.testNumberErrorItem()).should.eventually.contain('Enter a number.')
          .getText(TestErrorsPage.testPercentErrorItem()).should.eventually.contain('Enter an answer less than or equal to 100.')
          .getText(TestErrorsPage.testCurrencyErrorItem()).should.eventually.contain('Enter a number rounded to 2 decimal places.');
    });
  });


  it('Given a survey has an error when errors message is clicked then the correct answer is focused', function() {
    return helpers.openQuestionnaire('test_error_messages.json').then(() => {
        return browser
          .setValue(TestErrorsPage.testNumber(), 'cat')
          .setValue(TestErrorsPage.testPercent(), '101')
          .setValue(TestErrorsPage.testCurrency(), '123.456')
          .click(TestErrorsPage.submit())

          .click(TestErrorsPage.errorNumber(2))
          .hasFocus(TestErrorsPage.testPercent())
          .click(TestErrorsPage.errorNumber(3))
          .hasFocus(TestErrorsPage.testCurrency())
          .click(TestErrorsPage.errorNumber(1))
          .hasFocus(TestErrorsPage.testNumber());
    });
  });

});

