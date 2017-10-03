const helpers = require('../helpers');

const TestErrorsPage = require('../pages/surveys/error_messages/test-errors.page.js');

describe('Error Messages', function() {

  it('Given a survey has an error when errors are displayed then page error messages are correct', function() {
    return helpers.openQuestionnaire('test_error_messages.json').then(() => {
        return browser
          .setValue(TestErrorsPage.testNumber(), 'cat')
          .setValue(TestErrorsPage.testPercent(), '101')
          .setValue(TestErrorsPage.testCurrency(), '123.456')
          .click(TestErrorsPage.submit())

          .getText(TestErrorsPage.errorNumber(1)).should.eventually.contain('Enter a number.')
          .getText(TestErrorsPage.errorNumber(2)).should.eventually.contain('Enter a number less than or equal to 100.')
          .getText(TestErrorsPage.errorNumber(3)).should.eventually.contain('Enter a number rounded to 2 decimal places.');
    });
  });

  it('Given a survey has an error when errors are displayed then answer error messages are correct', function() {
    return helpers.openQuestionnaire('test_error_messages.json').then(() => {
        return browser
          .setValue(TestErrorsPage.testNumber(), 'cat')
          .setValue(TestErrorsPage.testPercent(), '101')
          .setValue(TestErrorsPage.testCurrency(), '123.456')
          .click(TestErrorsPage.submit())

          .getText(TestErrorsPage.checkError('number')).should.eventually.contain('Enter a number.')
          .getText(TestErrorsPage.checkError('percent')).should.eventually.contain('Enter a number less than or equal to 100.')
          .getText(TestErrorsPage.checkError('currency')).should.eventually.contain('Enter a number rounded to 2 decimal places.');
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

