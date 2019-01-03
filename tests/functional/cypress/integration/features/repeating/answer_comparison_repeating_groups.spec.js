import {openQuestionnaire} from '../../../helpers/helpers.js'

const RepeatingComparison1BlockPage = require('../../../../generated_pages/repeating_answer_comparison/repeating-comparison-1-block.page.js');
const RepeatingComparison2BlockPage = require('../../../../generated_pages/repeating_answer_comparison/repeating-comparison-2-block.page.js');
const SummaryPage = require('../../../../generated_pages/repeating_answer_comparison/summary.page.js');

describe('Test repeating with answer comparisons', function() {

  beforeEach(function() {
    openQuestionnaire('test_repeating_answer_comparison.json');
  });

  it('Given we open the repeating comparison test When we enter different numbers, Then the question should repeat', function() {
    cy
      .get(RepeatingComparison1BlockPage.repeatingComparison1()).type(5)
      .get(RepeatingComparison1BlockPage.submit()).click()
      .get(RepeatingComparison2BlockPage.repeatingComparison2()).type(6)
      .get(RepeatingComparison2BlockPage.submit()).click()
      .get(RepeatingComparison2BlockPage.questionText()).stripText().should('contain', 'Enter a number');
  });

  it('Given we open the repeating comparison test When we enter the same numbers, Then the question should not repeat', function() {
    cy
      .get(RepeatingComparison1BlockPage.repeatingComparison1()).type(5)
      .get(RepeatingComparison1BlockPage.submit()).click()
      .get(RepeatingComparison2BlockPage.repeatingComparison2()).type(5)
      .get(RepeatingComparison2BlockPage.submit()).click()
      .get(SummaryPage.summaryQuestionText()).stripText().should('contain', 'Enter a number');
  });

  it('Given we enter three sets of different numbers and one set of the same numbers, Then it shows a summary of all the entered values', function() {
    completeRepeatingQuestions(3)
    cy
      .get(SummaryPage.repeatingComparison1Answer(0)).stripText().should('contain', 0)
      .get(SummaryPage.repeatingComparison2Answer(0)).stripText().should('contain', 1)
      .get(SummaryPage.repeatingComparison1Answer(1)).stripText().should('contain', 1)
      .get(SummaryPage.repeatingComparison2Answer(1)).stripText().should('contain', 2)
      .get(SummaryPage.repeatingComparison1Answer(2)).stripText().should('contain', 2)
      .get(SummaryPage.repeatingComparison2Answer(2)).stripText().should('contain', 3)
      .get(SummaryPage.repeatingComparison1Answer(3)).stripText().should('contain', 100)
      .get(SummaryPage.repeatingComparison2Answer(3)).stripText().should('contain', 100);
  });
});

function completeRepeatingQuestions(numberOfRepeats) {
  for (let i = 0; i < numberOfRepeats; i++) {
    cy
      .get(RepeatingComparison1BlockPage.repeatingComparison1()).type(i)
      .get(RepeatingComparison1BlockPage.submit()).click()
      .get(RepeatingComparison2BlockPage.repeatingComparison2()).type(i+1)
      .get(RepeatingComparison2BlockPage.submit()).click();
  }

  cy
    .get(RepeatingComparison1BlockPage.repeatingComparison1()).type(100)
    .get(RepeatingComparison1BlockPage.submit()).click()
    .get(RepeatingComparison2BlockPage.repeatingComparison2()).type(100)
    .get(RepeatingComparison2BlockPage.submit()).click();
}
