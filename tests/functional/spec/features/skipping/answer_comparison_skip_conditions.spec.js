const helpers = require('../../../helpers');

const Comparison1Page = require('../../../generated_pages/skip_condition_answer_comparison/comparison-1.page.js');
const Comparison2Page = require('../../../generated_pages/skip_condition_answer_comparison/comparison-2.page.js');

describe('Test skip condition answer comparisons', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_skip_condition_answer_comparison.json');
  });

  it('Given we start the skip condition survey, when we enter the same answers, then the interstitial should show that the answers are the same', function() {
    return browser
      .setValue(Comparison1Page.answer(), 1)
      .click(Comparison1Page.submit())
      .setValue(Comparison2Page.answer(), 1)
      .click(Comparison2Page.submit())
      .getText('p').should.eventually.contain('Your second number was equal to your first number');
    });
  it('Given we start the skip condition survey, when we enter a high number then a low number, then the interstitial should show that the answers are low then high', function() {
    return browser
      .setValue(Comparison1Page.answer(), 3)
      .click(Comparison1Page.submit())
      .setValue(Comparison2Page.answer(), 2)
      .click(Comparison2Page.submit())
      .getText('p').should.eventually.contain('Your first answer was greater than your second number');
    });
  it('Given we start the skip condition survey, when we enter a low number then a high number, then the interstitial should show that the answers are high then low', function() {
    return browser
      .setValue(Comparison1Page.answer(), 1)
      .click(Comparison1Page.submit())
      .setValue(Comparison2Page.answer(), 2)
      .click(Comparison2Page.submit())
      .getText('p').should.eventually.contain('Your first answer was less than your second number');
    });
});

