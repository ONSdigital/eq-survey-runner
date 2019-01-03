import {openQuestionnaire} from '../../../helpers/helpers.js'

const Comparison1Page = require('../../../../generated_pages/skip_condition_answer_comparison/comparison-1.page.js');
const Comparison2Page = require('../../../../generated_pages/skip_condition_answer_comparison/comparison-2.page.js');
const EqualsAnswersPage = require('../../../../generated_pages/skip_condition_answer_comparison/equals-answers.page.js');
const LessThanAnswersPage = require('../../../../generated_pages/skip_condition_answer_comparison/less-than-answers.page.js');
const GreaterThanAnswersPage = require('../../../../generated_pages/skip_condition_answer_comparison/greater-than-answers.page.js');

describe('Test skip condition answer comparisons', function() {

  beforeEach(function() {
    openQuestionnaire('test_skip_condition_answer_comparison.json');
  });

  it('Given we start the skip condition survey, when we enter the same answers, then the interstitial should show that the answers are the same', function() {
    cy
      .get(Comparison1Page.answer()).type(1)
      .get(Comparison1Page.submit()).click()
      .get(Comparison2Page.answer()).type(1)
      .get(Comparison2Page.submit()).click()
      .get(EqualsAnswersPage.interstitialHeader()).stripText().should('contain', 'Second equal first');
  });

  it('Given we start the skip condition survey, when we enter a high number then a low number, then the interstitial should show that the answers are low then high', function() {
    cy
      .get(Comparison1Page.answer()).type(3)
      .get(Comparison1Page.submit()).click()
      .get(Comparison2Page.answer()).type(2)
      .get(Comparison2Page.submit()).click()
      .get(LessThanAnswersPage.interstitialHeader()).stripText().should('contain', 'First greater than second');
  });

  it('Given we start the skip condition survey, when we enter a low number then a high number, then the interstitial should show that the answers are high then low', function() {
    cy
      .get(Comparison1Page.answer()).type(1)
      .get(Comparison1Page.submit()).click()
      .get(Comparison2Page.answer()).type(2)
      .get(Comparison2Page.submit()).click()
      .get(GreaterThanAnswersPage.interstitialHeader()).stripText().should('contain', 'First less than second');
  });
});

