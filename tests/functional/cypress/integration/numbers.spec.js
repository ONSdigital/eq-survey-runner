import {openQuestionnaire} from ../helpers/helpers.js
const SetMinMax = require('../generated_pages/numbers/set-min-max-block.page.js');
const TestMinMax = require('../generated_pages/numbers/test-min-max-block.page.js');
const SummaryPage = require('../generated_pages/numbers/summary.page');

describe('NumericRange', function() {

  const number_schema = 'test_numbers.json';

  beforeEach(function() {
    return helpers.openQuestionnaire(number_schema);
  });

  it ('Answer labels should have descriptions displayed', function() {
          .get(SetMinMax.setMinimumLabelDescription()).stripText().should('contain', "This is a description of the minimum value")
      .get(SetMinMax.setMaximumLabelDescription()).stripText().should('contain', "This is a description of the maximum value");
  });

  it('Given a max and min set, a user should be able to complete the survey obeying those ranges', function() {
          .get(SetMinMax.setMinimum()).type('10')
      .get(SetMinMax.setMaximum()).type('1020')
      .get(SetMinMax.submit()).click()
      .get(TestMinMax.testRange()).type('10')
      .get(TestMinMax.testMin()).type('123')
      .get(TestMinMax.testMax()).type('456')
      .get(TestMinMax.testPercent()).type('100')
      .get(TestMinMax.submit()).click()
      .url().should('contain', SummaryPage.pageName);
  });

  it('Given values outside of the allowed range then the correct error messages are displayed', function() {
          .get(SetMinMax.setMinimum()).type('10')
      .get(SetMinMax.setMaximum()).type('1020')
      .get(SetMinMax.submit()).click()
      .get(TestMinMax.testRange()).type('9')
      .get(TestMinMax.testRangeExclusive()).type('10')
      .get(TestMinMax.testMin()).type('0')
      .get(TestMinMax.testMax()).type('12345')
      .get(TestMinMax.testMinExclusive()).type('123')
      .get(TestMinMax.testMaxExclusive()).type('12345')
      .get(TestMinMax.testPercent()).type('101')
      .get(TestMinMax.testDecimal()).type('5.4')
      .get(TestMinMax.submit()).click()
      .get(TestMinMax.errorNumber(1)).stripText().should('contain', "Enter an answer more than or equal to 10.")
      .get(TestMinMax.errorNumber(2)).stripText().should('contain', "Enter an answer more than 10.")
      .get(TestMinMax.errorNumber(3)).stripText().should('contain', "Enter an answer more than or equal to 123.")
      .get(TestMinMax.errorNumber(4)).stripText().should('contain', "Enter an answer less than or equal to 1,234.")
      .get(TestMinMax.errorNumber(5)).stripText().should('contain', "Enter an answer more than 123.")
      .get(TestMinMax.errorNumber(6)).stripText().should('contain', "Enter an answer less than 1,234.")
      .get(TestMinMax.errorNumber(7)).stripText().should('contain', "Enter an answer less than or equal to 100.")
      .get(TestMinMax.errorNumber(8)).stripText().should('contain', "Enter an answer more than or equal to £10.00.");
  });

  it('Given values outside of the allowed decimal places then the correct error messages are displayed', function() {
          .get(SetMinMax.setMinimum()).type('10')
      .get(SetMinMax.setMaximum()).type('1020')
      .get(SetMinMax.submit()).click()
      .get(TestMinMax.testRange()).type('12.344')
      .get(TestMinMax.testDecimal()).type('11.234')
      .get(TestMinMax.submit()).click()
      .get(TestMinMax.errorNumber(1)).stripText().should('contain', "Enter a number rounded to 2 decimal places.")
      .get(TestMinMax.errorNumber(2)).stripText().should('contain', "Enter a number rounded to 2 decimal places.");
  });
});
