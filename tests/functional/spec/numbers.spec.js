const helpers = require('../helpers');
const SetMinMax = require('../generated_pages/numbers/set-min-max-block.page.js');
const TestMinMax = require('../generated_pages/numbers/test-min-max-block.page.js');
const SummaryPage = require('../generated_pages/numbers/summary.page');

describe('NumericRange', function() {
  let browser;

  const number_schema = 'test_numbers.json';

  beforeEach(function() {
    browser = helpers.openQuestionnaire(number_schema).then(openBrowser => browser = openBrowser);
  });

  it ('Answer labels should have descriptions displayed', function() {
      expect($(SetMinMax.setMinimumLabelDescription()).getText()).to.contain("This is a description of the minimum value");
      expect($(SetMinMax.setMaximumLabelDescription()).getText()).to.contain("This is a description of the maximum value");
  });

  it('Given a max and min set, a user should be able to complete the survey obeying those ranges', function() {
      $(SetMinMax.setMinimum()).setValue('10');
      $(SetMinMax.setMaximum()).setValue('1020');
      $(SetMinMax.submit()).click();
      $(TestMinMax.testRange()).setValue('10');
      $(TestMinMax.testMin()).setValue('123');
      $(TestMinMax.testMax()).setValue('456');
      $(TestMinMax.testPercent()).setValue('100');
      $(TestMinMax.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  });

  it('Given values outside of the allowed range then the correct error messages are displayed', function() {
      $(SetMinMax.setMinimum()).setValue('10');
      $(SetMinMax.setMaximum()).setValue('1020');
      $(SetMinMax.submit()).click();
      $(TestMinMax.testRange()).setValue('9');
      $(TestMinMax.testRangeExclusive()).setValue('10');
      $(TestMinMax.testMin()).setValue('0');
      $(TestMinMax.testMax()).setValue('12345');
      $(TestMinMax.testMinExclusive()).setValue('123');
      $(TestMinMax.testMaxExclusive()).setValue('12345');
      $(TestMinMax.testPercent()).setValue('101');
      $(TestMinMax.testDecimal()).setValue('5.4');
      $(TestMinMax.submit()).click();
      expect($(TestMinMax.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to 10.");
      expect($(TestMinMax.errorNumber(2)).getText()).to.contain("Enter an answer more than 10.");
      expect($(TestMinMax.errorNumber(3)).getText()).to.contain("Enter an answer more than or equal to 123.");
      expect($(TestMinMax.errorNumber(4)).getText()).to.contain("Enter an answer less than or equal to 1,234.");
      expect($(TestMinMax.errorNumber(5)).getText()).to.contain("Enter an answer more than 123.");
      expect($(TestMinMax.errorNumber(6)).getText()).to.contain("Enter an answer less than 1,234.");
      expect($(TestMinMax.errorNumber(7)).getText()).to.contain("Enter an answer less than or equal to 100.");
      expect($(TestMinMax.errorNumber(8)).getText()).to.contain("Enter an answer more than or equal to £10.00.");
  });

  it('Given values outside of the allowed decimal places then the correct error messages are displayed', function() {
      $(SetMinMax.setMinimum()).setValue('10');
      $(SetMinMax.setMaximum()).setValue('1020');
      $(SetMinMax.submit()).click();
      $(TestMinMax.testRange()).setValue('12.344');
      $(TestMinMax.testDecimal()).setValue('11.234');
      $(TestMinMax.submit()).click();
      expect($(TestMinMax.errorNumber(1)).getText()).to.contain("Enter a number rounded to 2 decimal places.");
      expect($(TestMinMax.errorNumber(2)).getText()).to.contain("Enter a number rounded to 2 decimal places.");
  });
});
