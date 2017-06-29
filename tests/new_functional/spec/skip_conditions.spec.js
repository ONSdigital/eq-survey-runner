const helpers = require('../helpers');
const ShouldSkipPage = require('../pages/surveys/skip_conditions/do-you-want-to-skip.page');
const SkippedPage = require('../pages/surveys/skip_conditions/should-skip.page');
const SummaryPage = require('../pages/surveys/skip_conditions/summary.page');

describe('Skip Conditions', function() {

  it('Given I am not skipping, When I complete all questions, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_question.json').then(() => {
      return browser
        .click(ShouldSkipPage.firstNo())
        .click(ShouldSkipPage.secondNo())
        .click(ShouldSkipPage.submit())
        .click(SkippedPage.skippedOneNo())
        .click(SkippedPage.skipTwoNo())
        .click(SkippedPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

  it('Given metadata is choosing to skip, When I complete all questions, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_question.json', 'Skip').then(() => {
      return browser
        .click(ShouldSkipPage.firstNo())
        .click(ShouldSkipPage.secondNo())
        .click(ShouldSkipPage.submit())
        .click(SkippedPage.skippedOneYes())
        .click(SkippedPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

  it('Given first question is choosing to skip, When I complete all questions, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_question.json').then(() => {
      return browser
        .click(ShouldSkipPage.firstYes())
        .click(ShouldSkipPage.secondNo())
        .click(ShouldSkipPage.submit())
        .click(SkippedPage.skippedOneYes())
        .click(SkippedPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

  it('Given second question is choosing to skip, When I complete all questions, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_question.json').then(() => {
      return browser
        .click(ShouldSkipPage.firstNo())
        .click(ShouldSkipPage.secondYes())
        .click(ShouldSkipPage.submit())
        .click(SkippedPage.skippedOneYes())
        .click(SkippedPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

  it('Given both questions are choosing to skip, When I complete all questions, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_question.json').then(() => {
      return browser
        .click(ShouldSkipPage.firstYes())
        .click(ShouldSkipPage.secondYes())
        .click(ShouldSkipPage.submit())
        .click(SkippedPage.skippedOneYes())
        .click(SkippedPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

  it('Given both questions and metadata are choosing to skip, When I complete all questions, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_question.json', 'Skip').then(() => {
      return browser
        .click(ShouldSkipPage.firstYes())
        .click(ShouldSkipPage.secondYes())
        .click(ShouldSkipPage.submit())
        .click(SkippedPage.skippedOneYes())
        .click(SkippedPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

});
