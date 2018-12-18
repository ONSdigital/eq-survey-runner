import {openQuestionnaire} from ../../../helpers/helpers.js
const DefaultTitlePage = require('../../../generated_pages/titles/single-title-block.page');
const SingleTitlePage = require('../../../generated_pages/titles/who-is-answering-block.page');
const ConditionalTitlePage = require('../../../generated_pages/titles/multiple-question-versions-block.page');
const SummaryPage = require('../../../generated_pages/titles/summary.page');


describe('Feature: Conditional question title', function() {

  beforeEach(function() {
      return helpers.openQuestionnaire('test_titles.json');
  });
  describe('Given I start the different version of question titles survey', function() {
    it('When I am on the first page, Then I should see the default value for a question title', function() {
             .get(DefaultTitlePage.questionText()).stripText().should('contain', 'How are you feeling??');
    });
   });

  describe('Given I start the different version of question titles survey', function() {
    it('When I navigate to the second page, Then I should see a single title value', function() {
              .get().click()
        .get().click()
        .get(SingleTitlePage.questionText()).stripText().should('contain', 'Who are you answering on behalf of?');
    });
  });

  describe('Given I start the different version of question titles survey', function() {
    it('When I navigate through the survey, Then I should see the correct page titles', function() {
              .getTitle().should.eventually.contain('How are you feeling?? - Multiple Question Title Test')
        .get().click()
        .get().click()
        .getTitle().should.eventually.contain('Who are you answering on behalf of? - Multiple Question Title Test')
        .get().click()
        .get().click()
        .getTitle().should.eventually.contain('What is … gender? - Multiple Question Title Test')
        .get().click()
        .get(ConditionalTitlePage.age()).type('25')
        .get().click()
        .get().click()
        .getTitle().should.eventually.contain('Summary - Multiple Question Title Test');
    });
  });



  describe('Given I start the different version of question titles survey', function() {
    beforeEach(function() {
              .get().click()
        .get().click();
  });
    it('When I navigate to the proxy question and select Chad, Then I should see versions of questions aimed at Chad on the next page', function() {
              .get().click()
        .get().click()
        .get(ConditionalTitlePage.questionText()).stripText().should('contain', 'What is chad’s gender?')
        .get(ConditionalTitlePage.questionText()).stripText().should('contain', 'What is chad’s age?');
    });

    it('When I navigate to the proxy question and select Kelly, Then I should see versions of questions aimed at Kelly on the next page', function() {
              .get().click()
        .get().click()
        .get(ConditionalTitlePage.questionText()).stripText().should('contain', 'What is kelly’s gender?')
        .get(ConditionalTitlePage.questionText()).stripText().should('contain', 'What is kelly’s age?');
    });

    it('When I navigate to the proxy question and select Someone else, Then I should see versions of questions aimed at a 3rd person on the next page', function() {
              .get(SingleTitlePage.else()).click()
        .get(SingleTitlePage.submit()).click()
        .get(ConditionalTitlePage.questionText()).stripText().should('contain', 'What is their gender?')
        .get(ConditionalTitlePage.questionText()).stripText().should('contain', 'What is their age?');
    });

    it('When I navigate to the proxy question and select myself, Then I should see versions of questions aimed at myself on the next page', function() {
              .get(SingleTitlePage.myself()).click()
        .get(SingleTitlePage.submit()).click()
        .get(ConditionalTitlePage.questionText()).stripText().should('contain', 'What is your gender?')
        .get(ConditionalTitlePage.questionText()).stripText().should('contain', 'What is your age?');
    });
  });

  describe('Given I start the different version of question titles survey', function() {
    it('When I navigate to the summary having selected a default title, and single title and a condition title, Then I should see correct question titles rendered on the summary page', function() {
              .get(DefaultTitlePage.good()).click()
        .get(DefaultTitlePage.submit()).click()
        .get(SingleTitlePage.chad()).click()
        .get(SingleTitlePage.submit()).click()
        .get(ConditionalTitlePage.genderMale()).click()
        .get(ConditionalTitlePage.age()).type('25')
        .get(ConditionalTitlePage.sureYes()).click()
        .get(SingleTitlePage.submit()).click()
        .get(SummaryPage.summaryQuestionText()).stripText().should('contain', 'How are you feeling??')
        .get(SummaryPage.summaryQuestionText()).stripText().should('contain', 'Who are you answering on behalf of?')
        .get(SummaryPage.summaryQuestionText()).stripText().should('contain', 'What is chad’s gender?')
        .get(SummaryPage.summaryQuestionText()).stripText().should('contain', 'What is chad’s age?');
    });
  });
});
