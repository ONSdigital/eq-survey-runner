import {openQuestionnaire} from '../helpers/helpers.js';
const ShouldSkipPage = require('../../generated_pages/skip_condition_question/do-you-want-to-skip.page');
const SkippedPage = require('../../generated_pages/skip_condition_question/should-skip.page');
const SummaryPage = require('../../generated_pages/skip_condition_question/summary.page');



describe('Skip Conditions', function() {
  describe('With metadata',() => {
    beforeEach(() => {
      openQuestionnaire('test_skip_condition_question.json', { userId: 'Skip' });
    });

    it('Given metadata is choosing to skip, When I complete all questions, Then I should see the summary page', function() {
      cy
        .get(ShouldSkipPage.firstNo()).click()
        .get(ShouldSkipPage.secondNo()).click()
        .get(ShouldSkipPage.submit()).click()
        .get(SkippedPage.skippedOneYes()).click()
        .get(SkippedPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });

    it('Given metadata is choosing to skip, When I complete all questions, Then I should see the summary page', function() {
      cy
        .get(ShouldSkipPage.firstNo()).click()
        .get(ShouldSkipPage.secondNo()).click()
        .get(ShouldSkipPage.submit()).click()
        .get(SkippedPage.skippedOneYes()).click()
        .get(SkippedPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });

  });

  describe('Without metadata', () => {
    beforeEach(() => {
      openQuestionnaire('test_skip_condition_question.json');
    });

    it('Given I am not skipping, When I complete all questions, Then I should see the summary page', function() {
      cy
        .get(ShouldSkipPage.firstNo()).click()
        .get(ShouldSkipPage.secondNo()).click()
        .get(ShouldSkipPage.submit()).click()
        .get(SkippedPage.skippedOneNo()).click()
        .get(SkippedPage.skipTwoNo()).click()
        .get(SkippedPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });

    it('Given first question is choosing to skip, When I complete all questions, Then I should see the summary page', function() {
      cy
        .get(ShouldSkipPage.firstYes()).click()
        .get(ShouldSkipPage.secondNo()).click()
        .get(ShouldSkipPage.submit()).click()
        .get(SkippedPage.skippedOneYes()).click()
        .get(SkippedPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });

    it('Given second question is choosing to skip, When I complete all questions, Then I should see the summary page', function() {
      cy
        .get(ShouldSkipPage.firstNo()).click()
        .get(ShouldSkipPage.secondYes()).click()
        .get(ShouldSkipPage.submit()).click()
        .get(SkippedPage.skippedOneYes()).click()
        .get(SkippedPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });

    it('Given both questions are choosing to skip, When I complete all questions, Then I should see the summary page', function() {
      cy
        .get(ShouldSkipPage.firstYes()).click()
        .get(ShouldSkipPage.secondYes()).click()
        .get(ShouldSkipPage.submit()).click()
        .get(SkippedPage.skippedOneYes()).click()
        .get(SkippedPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });

    it('Given both questions and metadata are choosing to skip, When I complete all questions, Then I should see the summary page', function() {
      cy
        .get(ShouldSkipPage.firstYes()).click()
        .get(ShouldSkipPage.secondYes()).click()
        .get(ShouldSkipPage.submit()).click()
        .get(SkippedPage.skippedOneYes()).click()
        .get(SkippedPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });

  });

});
