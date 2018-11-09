const helpers = require('../helpers');
const SetMinMax = require('../generated_pages/numbers/set-min-max-block.page.js');
const TestMinMax = require('../generated_pages/numbers/test-min-max-block.page.js');
const SummaryPage = require('../generated_pages/numbers/summary.page');

describe('NumericRange', function() {

  const number_schema = 'test_numbers.json';

  beforeEach(function() {
    return helpers.openQuestionnaire(number_schema);
  });

  it ('Answer labels should have descriptions displayed', function() {
    return browser
      .getText(SetMinMax.setMinimumLabelDescription()).should.eventually.contain("This is a description of the minimum value")
      .getText(SetMinMax.setMaximumLabelDescription()).should.eventually.contain("This is a description of the maximum value");
  });

  it('Given a max and min set, a user should be able to complete the survey obeying those ranges', function() {
    return browser
      .setValue(SetMinMax.setMinimum(), '10')
      .setValue(SetMinMax.setMaximum(), '1020')
      .click(SetMinMax.submit())
      .setValue(TestMinMax.testRange(), '10')
      .setValue(TestMinMax.testMin(), '123')
      .setValue(TestMinMax.testMax(), '456')
      .setValue(TestMinMax.testPercent(), '100')
      .click(TestMinMax.submit())
      .getUrl().should.eventually.contain(SummaryPage.pageName);
  });

  it('Given values outside of the allowed range then the correct error messages are displayed', function() {
    return browser
      .setValue(SetMinMax.setMinimum(), '10')
      .setValue(SetMinMax.setMaximum(), '1020')
      .click(SetMinMax.submit())
      .setValue(TestMinMax.testRange(), '9')
      .setValue(TestMinMax.testRangeExclusive(), '10')
      .setValue(TestMinMax.testMin(), '0')
      .setValue(TestMinMax.testMax(), '12345')
      .setValue(TestMinMax.testMinExclusive(), '123')
      .setValue(TestMinMax.testMaxExclusive(), '12345')
      .setValue(TestMinMax.testPercent(), '101')
      .setValue(TestMinMax.testDecimal(), '5.4')
      .click(TestMinMax.submit())
      .getText(TestMinMax.errorNumber(1)).should.eventually.contain("Enter an answer more than or equal to 10.")
      .getText(TestMinMax.errorNumber(2)).should.eventually.contain("Enter an answer more than 10.")
      .getText(TestMinMax.errorNumber(3)).should.eventually.contain("Enter an answer more than or equal to 123.")
      .getText(TestMinMax.errorNumber(4)).should.eventually.contain("Enter an answer less than or equal to 1,234.")
      .getText(TestMinMax.errorNumber(5)).should.eventually.contain("Enter an answer more than 123.")
      .getText(TestMinMax.errorNumber(6)).should.eventually.contain("Enter an answer less than 1,234.")
      .getText(TestMinMax.errorNumber(7)).should.eventually.contain("Enter an answer less than or equal to 100.")
      .getText(TestMinMax.errorNumber(8)).should.eventually.contain("Enter an answer more than or equal to £10.00.");
  });

  it('Given values outside of the allowed decimal places then the correct error messages are displayed', function() {
    return browser
      .setValue(SetMinMax.setMinimum(), '10')
      .setValue(SetMinMax.setMaximum(), '1020')
      .click(SetMinMax.submit())
      .setValue(TestMinMax.testRange(), '12.344')
      .setValue(TestMinMax.testDecimal(), '11.234')
      .click(TestMinMax.submit())
      .getText(TestMinMax.errorNumber(1)).should.eventually.contain("Enter a number rounded to 2 decimal places.")
      .getText(TestMinMax.errorNumber(2)).should.eventually.contain("Enter a number rounded to 2 decimal places.");
  });
});
