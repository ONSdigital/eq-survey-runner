const helpers = require('../helpers');

const BreakDownPage = require('../generated_pages/total_breakdown/block.page.js');

const highlightedInput = '[class$=input--has-error]';

describe('Total Breakdown', function() {

  it('Given four percentage fields, When I enter 10, 20, 30 and 40 in the field, Then total should be 100', function() {
    return helpers.openQuestionnaire('test_total_breakdown.json').then(() => {
      return browser
        .setValue(BreakDownPage.percentage1(), '10')
        .setValue(BreakDownPage.percentage2(), '20')
        .setValue(BreakDownPage.percentage3(), '30')
        .setValue(BreakDownPage.percentage4(), '40')
        .click(BreakDownPage.totalPercentageLabel())
        .getValue(BreakDownPage.totalPercentage()).should.eventually.contain('100');
    });
  });

  it('Given four percentage fields, When I enter non integer value into a field, Then total should ignore the non integer value', function() {
    return helpers.openQuestionnaire('test_total_breakdown.json').then(() => {
      return browser
        .setValue(BreakDownPage.percentage1(), 'ten')
        .setValue(BreakDownPage.percentage2(), '20')
        .setValue(BreakDownPage.percentage3(), '30')
        .setValue(BreakDownPage.percentage4(), '40')
        .click(BreakDownPage.totalPercentageLabel())
        .getValue(BreakDownPage.totalPercentage()).should.eventually.contain('90');
    });
  });

  it('Given four percentage fields, When I enter a negative value into a field, Then total should ignore the negative value', function() {
    return helpers.openQuestionnaire('test_total_breakdown.json').then(() => {
      return browser
        .setValue(BreakDownPage.percentage1(), '-10')
        .setValue(BreakDownPage.percentage2(), '20')
        .setValue(BreakDownPage.percentage3(), '30')
        .setValue(BreakDownPage.percentage4(), '40')
        .click(BreakDownPage.totalPercentageLabel())
        .getValue(BreakDownPage.totalPercentage()).should.eventually.contain('90');
    });
  });

  it('Given four percentage fields, When I enter a values totalling > 100, Then total should display the value', function() {
  return helpers.openQuestionnaire('test_total_breakdown.json').then(() => {
    return browser
      .setValue(BreakDownPage.percentage1(), '20')
      .setValue(BreakDownPage.percentage2(), '30')
      .setValue(BreakDownPage.percentage3(), '40')
      .setValue(BreakDownPage.percentage4(), '50')
      .click(BreakDownPage.totalPercentageLabel())
      .getValue(BreakDownPage.totalPercentage()).should.eventually.contain('140');
    });
  });

  it('Given four percentage fields, When I enter non-integer values into each field, Then total should be 0', function() {
  return helpers.openQuestionnaire('test_total_breakdown.json').then(() => {
    return browser
      .setValue(BreakDownPage.percentage1(), 'ten')
      .setValue(BreakDownPage.percentage2(), 'twenty')
      .setValue(BreakDownPage.percentage3(), 'thirty')
      .setValue(BreakDownPage.percentage4(), 'forty')
      .click(BreakDownPage.totalPercentageLabel())
      .getValue(BreakDownPage.totalPercentage()).should.eventually.contain('0');
    });
  });

  it('Given four percentage fields, When total is not 100, Then total field should be highlighted', function() {
  return helpers.openQuestionnaire('test_total_breakdown.json').then(() => {
    return browser
      .setValue(BreakDownPage.percentage1(), '1')
      .setValue(BreakDownPage.percentage2(), '2')
      .setValue(BreakDownPage.percentage3(), '3')
      .setValue(BreakDownPage.percentage4(), '4')
      .click(BreakDownPage.totalPercentageLabel())
      .isExisting(highlightedInput)

      .setValue(BreakDownPage.percentage4(), '100')
      .click(BreakDownPage.totalPercentageLabel())
      .isExisting(highlightedInput)

      .setValue(BreakDownPage.percentage4(), '94')
      .click(BreakDownPage.totalPercentageLabel())
      .isExisting(highlightedInput);
    });
  });

  it('Given four percentage fields, When floating point numbers entered, Then total should be integer', function() {
  return helpers.openQuestionnaire('test_total_breakdown.json').then(() => {
    return browser
      .setValue(BreakDownPage.percentage1(), '1.234')
      .setValue(BreakDownPage.percentage2(), '2.345')
      .setValue(BreakDownPage.percentage3(), '3.456')
      .setValue(BreakDownPage.percentage4(), '4.567')
      .click(BreakDownPage.totalPercentageLabel())
      .getValue(BreakDownPage.totalPercentage()).should.eventually.contain('10');
    });
  });

  it('Given a total field, When I navigate away then come back, Then total value should be preserved', function() {
  return helpers.openQuestionnaire('test_total_breakdown.json').then(() => {
    return browser
      .setValue(BreakDownPage.percentage1(), '1')
      .setValue(BreakDownPage.percentage2(), '2')
      .setValue(BreakDownPage.percentage3(), '3')
      .setValue(BreakDownPage.percentage4(), '4')
      .click(BreakDownPage.submit())
      .click(BreakDownPage.previous())
      .getValue(BreakDownPage.totalPercentage()).should.eventually.contain('10');
    });
  });

});

