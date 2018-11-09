const helpers = require('../../../helpers');

const Comparison1Page = require('../../../generated_pages/skip_condition_answer_comparison/comparison-1.page.js');
const Comparison2Page = require('../../../generated_pages/skip_condition_answer_comparison/comparison-2.page.js');
const EqualsAnswersPage = require('../../../generated_pages/skip_condition_answer_comparison/equals-answers.page.js');
const LessThanAnswersPage = require('../../../generated_pages/skip_condition_answer_comparison/less-than-answers.page.js');
const GreaterThanAnswersPage = require('../../../generated_pages/skip_condition_answer_comparison/greater-than-answers.page.js');

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
      .getText(EqualsAnswersPage.interstitialHeader()).should.eventually.contain('Second equal first');
    });
  it('Given we start the skip condition survey, when we enter a high number then a low number, then the interstitial should show that the answers are low then high', function() {
    return browser
      .setValue(Comparison1Page.answer(), 3)
      .click(Comparison1Page.submit())
      .setValue(Comparison2Page.answer(), 2)
      .click(Comparison2Page.submit())
      .getText(LessThanAnswersPage.interstitialHeader()).should.eventually.contain('First greater than second');
    });
  it('Given we start the skip condition survey, when we enter a low number then a high number, then the interstitial should show that the answers are high then low', function() {
    return browser
      .setValue(Comparison1Page.answer(), 1)
      .click(Comparison1Page.submit())
      .setValue(Comparison2Page.answer(), 2)
      .click(Comparison2Page.submit())
      .getText(GreaterThanAnswersPage.interstitialHeader()).should.eventually.contain('First less than second');
    });
});

