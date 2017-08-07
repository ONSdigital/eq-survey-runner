const helpers = require('../helpers');
const SetMinMax = require('../pages/surveys/numbers/set-min-max-block.page.js');
const TestMinMax = require('../pages/surveys/numbers/test-min-max-block.page.js');
const SummaryPage = require('../pages/surveys/skip_conditions/summary.page');

describe('NumericRange', function() {

  const number_schema = 'test_numbers.json';

  it('Given a max and min set, a user should be able to complete the survey obeying those ranges', function() {
    return helpers.openQuestionnaire(number_schema)
      .then(() => {
        return browser
          .setValue(SetMinMax.setMinimum(), '10')
          .setValue(SetMinMax.setMaximum(), '20')
          .click(SetMinMax.submit())
          .setValue(TestMinMax.testRange(), '10')
          .setValue(TestMinMax.testMin(), '123')
          .setValue(TestMinMax.testMax(), '456')
          .setValue(TestMinMax.testPercent(), '100')
          .click(TestMinMax.submit())
          .getUrl().should.eventually.contain(SummaryPage.pageName);
      });
  });

  it('Given values outside of the allowed range then the correct error messages are displayed', function() {
    return helpers.openQuestionnaire(number_schema)
      .then(() => {
        return browser
          .setValue(SetMinMax.setMinimum(), '10')
          .setValue(SetMinMax.setMaximum(), '20')
          .click(SetMinMax.submit())
          .setValue(TestMinMax.testRange(), '9')
          .setValue(TestMinMax.testMin(), '0')
          .setValue(TestMinMax.testMax(), '789')
          .setValue(TestMinMax.testPercent(), '101')
          .click(TestMinMax.submit())
          .getText('ul > li:nth-child(1) > a').should.eventually.contain('The value must be between 10 and 20. Please correct your answer.')
          .getText('ul > li:nth-child(2) > a').should.eventually.contain('The minimum value allowed is 123. Please correct your answer.')
          .getText('ul > li:nth-child(3) > a').should.eventually.contain('The maximum value allowed is 456. Please correct your answer.')
          .getText('ul > li:nth-child(4) > a').should.eventually.contain('Percentages must be between 0 and 100.');
      });
  });

  it('Given values outside of the allowed decimal places then the correct error messages are displayed', function() {
    return helpers.openQuestionnaire(number_schema)
      .then(() => {
        return browser
          .setValue(SetMinMax.setMinimum(), '10')
          .setValue(SetMinMax.setMaximum(), '20')
          .click(SetMinMax.submit())
          .setValue(TestMinMax.testRange(), '12.3')
          .setValue(TestMinMax.testDecimal(), '1.234')
          .click(TestMinMax.submit())
          .getText('ul > li:nth-child(1) > a').should.eventually.contain('Please only enter numbers to 0 decimal places into the field.')
          .getText('ul > li:nth-child(2) > a').should.eventually.contain('Please only enter numbers to 2 decimal places into the field.');
      });
  });

});
