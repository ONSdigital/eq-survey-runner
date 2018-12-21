import {openQuestionnaire} from '../helpers/helpers.js'

const BreakDownPage = require('../../generated_pages/total_breakdown/block.page.js');

const highlightedInput = '[class$=input--has-error]';

describe('Total Breakdown', function() {
  beforeEach(() => {
    openQuestionnaire('test_total_breakdown.json')
  })

  it('Given four percentage fields, When I enter 10, 20, 30 and 40 in the field, Then total should be 100', function() {
    cy
      .get(BreakDownPage.percentage1()).type('10')
      .get(BreakDownPage.percentage2()).type('20')
      .get(BreakDownPage.percentage3()).type('30')
      .get(BreakDownPage.percentage4()).type('40')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get(BreakDownPage.totalPercentage()).invoke('val').should('contain', '100');
  });

  it('Given four percentage fields, When I enter non integer value into a field, Then total should ignore the non integer value', function() {
    cy
      .get(BreakDownPage.percentage1()).type('ten')
      .get(BreakDownPage.percentage2()).type('20')
      .get(BreakDownPage.percentage3()).type('30')
      .get(BreakDownPage.percentage4()).type('40')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get(BreakDownPage.totalPercentage()).invoke('val').should('contain', '90');
  });

  it('Given four percentage fields, When I enter a negative value into a field, Then total should ignore the negative value', function() {
    cy
      .get(BreakDownPage.percentage1()).type('-10')
      .get(BreakDownPage.percentage2()).type('20')
      .get(BreakDownPage.percentage3()).type('30')
      .get(BreakDownPage.percentage4()).type('40')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get(BreakDownPage.totalPercentage()).invoke('val').should('contain', '90');
  });

  it('Given four percentage fields, When I enter a values totalling > 100, Then total should display the value', function() {
    cy
      .get(BreakDownPage.percentage1()).type('20')
      .get(BreakDownPage.percentage2()).type('30')
      .get(BreakDownPage.percentage3()).type('40')
      .get(BreakDownPage.percentage4()).type('50')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get(BreakDownPage.totalPercentage()).invoke('val').should('contain', '140');
  });

  it('Given four percentage fields, When I enter non-integer values into each field, Then total should be 0', function() {
    cy
      .get(BreakDownPage.percentage1()).type('ten')
      .get(BreakDownPage.percentage2()).type('twenty')
      .get(BreakDownPage.percentage3()).type('thirty')
      .get(BreakDownPage.percentage4()).type('forty')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get(BreakDownPage.totalPercentage()).invoke('val').should('contain', '0');
  });

  it('Given four percentage fields, When total is not 100, Then total field should be highlighted', function() {
    cy
      .get(BreakDownPage.percentage1()).type('1')
      .get(BreakDownPage.percentage2()).type('2')
      .get(BreakDownPage.percentage3()).type('3')
      .get(BreakDownPage.percentage4()).type('4')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get(highlightedInput).should('exist')

      .get(BreakDownPage.percentage4()).type('100')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get((highlightedInput)).should('exist')

      .get(BreakDownPage.percentage4()).type('94')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get((highlightedInput)).should('exist')
  });

  it('Given four percentage fields, When floating point numbers entered, Then total should be a floating point number', function() {
    cy
      .get(BreakDownPage.percentage1()).type('1.23')
      .get(BreakDownPage.percentage2()).type('2.35')
      .get(BreakDownPage.percentage3()).type('3.45')
      .get(BreakDownPage.percentage4()).type('4.56')
      .get(BreakDownPage.totalPercentageLabel()).click()
      .get(BreakDownPage.totalPercentage()).invoke('val').should('contain', '11.59');
  });

  it('Given a total field, When I navigate away then come back, Then total value should be preserved', function() {
    cy
      .get(BreakDownPage.percentage1()).type('1')
      .get(BreakDownPage.percentage2()).type('2')
      .get(BreakDownPage.percentage3()).type('3')
      .get(BreakDownPage.percentage4()).type('4')
      .get(BreakDownPage.submit()).click()
      .get(BreakDownPage.previous()).click()
      .get(BreakDownPage.totalPercentage()).invoke('val').should('contain', '10');
  });

});

