const helpers = require('../../../helpers');

const RepeatingComparison1BlockPage = require('../../../generated_pages/repeating_answer_comparison/repeating-comparison-1-block.page.js');
const RepeatingComparison2BlockPage = require('../../../generated_pages/repeating_answer_comparison/repeating-comparison-2-block.page.js');
const SummaryPage = require('../../../generated_pages/repeating_answer_comparison/summary.page.js');

describe('Test repeating with answer comparisons', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_repeating_answer_comparison.json');
  });

  it('Given we open the repeating comparison test When we enter different numbers, Then the question should repeat', function() {
    return browser
      .setValue(RepeatingComparison1BlockPage.repeatingComparison1(), 5)
      .click(RepeatingComparison1BlockPage.submit())
      .setValue(RepeatingComparison2BlockPage.repeatingComparison2(), 6)
      .click(RepeatingComparison2BlockPage.submit())
      .getText(RepeatingComparison2BlockPage.questionText()).should.eventually.contain('Enter a number');
  });

  it('Given we open the repeating comparison test When we enter the same numbers, Then the question should not repeat', function() {
    return browser
      .setValue(RepeatingComparison1BlockPage.repeatingComparison1(), 5)
      .click(RepeatingComparison1BlockPage.submit())
      .setValue(RepeatingComparison2BlockPage.repeatingComparison2(), 5)
      .click(RepeatingComparison2BlockPage.submit())
      .getText(SummaryPage.summaryQuestionText()).should.eventually.contain('Enter a number');
  });

  it('Given we enter three sets of different numbers and one set of the same numbers, Then it shows a summary of all the entered values', function() {
    return completeRepeatingQuestions(3)
      .then(() => {
        return browser
          .getText(SummaryPage.repeatingComparison1Answer(0)).should.eventually.contain(0)
          .getText(SummaryPage.repeatingComparison2Answer(0)).should.eventually.contain(1)
          .getText(SummaryPage.repeatingComparison1Answer(1)).should.eventually.contain(1)
          .getText(SummaryPage.repeatingComparison2Answer(1)).should.eventually.contain(2)
          .getText(SummaryPage.repeatingComparison1Answer(2)).should.eventually.contain(2)
          .getText(SummaryPage.repeatingComparison2Answer(2)).should.eventually.contain(3)
          .getText(SummaryPage.repeatingComparison1Answer(3)).should.eventually.contain(100)
          .getText(SummaryPage.repeatingComparison2Answer(3)).should.eventually.contain(100);
      });
  });
});

function completeRepeatingQuestions(numberOfRepeats) {
  let chain = browser.pause(0);

  for (let i = 0; i < numberOfRepeats; i++) {
    chain = chain.then(() => {
      return browser
        .setValue(RepeatingComparison1BlockPage.repeatingComparison1(), i)
        .click(RepeatingComparison1BlockPage.submit())
        .setValue(RepeatingComparison2BlockPage.repeatingComparison2(), i+1)
        .click(RepeatingComparison2BlockPage.submit());
    });
  }

  chain = chain.then(() => {
    return browser
      .setValue(RepeatingComparison1BlockPage.repeatingComparison1(), 100)
      .click(RepeatingComparison1BlockPage.submit())
      .setValue(RepeatingComparison2BlockPage.repeatingComparison2(), 100)
      .click(RepeatingComparison2BlockPage.submit());
  });

  return chain;
}
