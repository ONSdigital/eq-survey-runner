const helpers = require('../helpers');

const TestErrorsPage = require('../generated_pages/error_messages/test-errors.page.js');

describe('Error Messages', function() {
  let browser;

  it('Given a survey has an error when errors are displayed then page error messages are correct', function() {
    browser = helpers.openQuestionnaire('test_error_messages.json');
    $(TestErrorsPage.testNumber()).setValue('cat');
    $(TestErrorsPage.testPercent()).setValue('101');
    $(TestErrorsPage.testCurrency()).setValue('123.456');
    $(TestErrorsPage.submit()).click();
    expect($(TestErrorsPage.errorHeader()).getText()).to.contain('This page has 3 errors');
    expect($(TestErrorsPage.errorNumber(1)).getText()).to.contain('Enter a number.');
    expect($(TestErrorsPage.errorNumber(2)).getText()).to.contain('Enter an answer less than or equal to 100.');
    expect($(TestErrorsPage.errorNumber(3)).getText()).to.contain('Enter a number rounded to 2 decimal places.');
  });

  it('Given a survey has 1 error when error is displayed then error header is displayed correct', function() {
    browser = helpers.openQuestionnaire('test_error_messages.json');
    $(TestErrorsPage.testNumber()).setValue('cat');
    $(TestErrorsPage.testPercent()).setValue('100');
    $(TestErrorsPage.testCurrency()).setValue('123.45');
    $(TestErrorsPage.submit()).click();
    expect($(TestErrorsPage.errorHeader()).getText()).to.contain('This page has an error');
  });

  it('Given a survey has an error when errors are displayed then answer error messages are correct', function() {
    browser = helpers.openQuestionnaire('test_error_messages.json');
    $(TestErrorsPage.testNumber()).setValue('cat');
    $(TestErrorsPage.testPercent()).setValue('101');
    $(TestErrorsPage.testCurrency()).setValue('123.456');
    $(TestErrorsPage.submit()).click();

    expect($(TestErrorsPage.testNumberErrorItem()).getText()).to.contain('Enter a number.');
    expect($(TestErrorsPage.testPercentErrorItem()).getText()).to.contain('Enter an answer less than or equal to 100.');
    expect($(TestErrorsPage.testCurrencyErrorItem()).getText()).to.contain('Enter a number rounded to 2 decimal places.');
  });


  it('Given a survey has an error when errors message is clicked then the correct answer is focused', function() {
    browser = helpers.openQuestionnaire('test_error_messages.json');
    $(TestErrorsPage.testNumber()).setValue('cat');
    $(TestErrorsPage.testPercent()).setValue('101');
    $(TestErrorsPage.testCurrency()).setValue('123.456');
    $(TestErrorsPage.submit()).click();

    $(TestErrorsPage.errorNumber(2)).click();
    expect($(TestErrorsPage.testPercent()).isFocused()).to.be.true;
    $(TestErrorsPage.errorNumber(3)).click();
    expect($(TestErrorsPage.testCurrency()).isFocused()).to.be.true;
    $(TestErrorsPage.errorNumber(1)).click();
    expect($(TestErrorsPage.testNumber()).isFocused()).to.be.true;
  });

});

