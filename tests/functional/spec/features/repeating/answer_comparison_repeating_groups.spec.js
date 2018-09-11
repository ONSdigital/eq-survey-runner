const helpers = require('../../../helpers');

const RepeatingComparison1BlockPage = require('../../../pages/features/answer_comparison/repeating_groups/repeating-comparison-1-block.page.js');
const RepeatingComparison2BlockPage = require('../../../pages/features/answer_comparison/repeating_groups/repeating-comparison-2-block.page.js');
const SummaryPage = require('../../../pages/features/answer_comparison/repeating_groups/summary.page.js');

describe('Test repeating with answer comparisons', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_repeating_answer_comparison.json');
  });

  it('Given we open the repeating comparison test When we enter different numbers, Then the question should repeat', function() {
    return browser
      .setValue(RepeatingComparison1BlockPage.answer(), 5)
      .click(RepeatingComparison1BlockPage.submit())
      .setValue(RepeatingComparison2BlockPage.answer(), 6)
      .click(RepeatingComparison2BlockPage.submit())
      .getText(RepeatingComparison2BlockPage.questionText()).should.eventually.contain('Enter a number');
  });

  it('Given we open the repeating comparison test When we enter the same numbers, Then the question should not repeat', function() {
    return browser
      .setValue(RepeatingComparison1BlockPage.answer(), 5)
      .click(RepeatingComparison1BlockPage.submit())
      .setValue(RepeatingComparison2BlockPage.answer(), 5)
      .click(RepeatingComparison2BlockPage.submit())
      .getText(SummaryPage.summaryQuestionText()).should.eventually.contain('Enter a number');
  });
});

