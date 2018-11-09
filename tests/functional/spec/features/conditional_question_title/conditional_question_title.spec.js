const helpers = require('../../../helpers');
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
      return browser
       .getText(DefaultTitlePage.questionText()).should.eventually.contain('How are you feeling??');
    });
   });

  describe('Given I start the different version of question titles survey', function() {
    it('When I navigate to the second page, Then I should see a single title value', function() {
      return browser
        .click(DefaultTitlePage.good())
        .click(DefaultTitlePage.submit())
        .getText(SingleTitlePage.questionText()).should.eventually.contain('Who are you answering on behalf of?');
    });
  });

  describe('Given I start the different version of question titles survey', function() {
    it('When I navigate through the survey, Then I should see the correct page titles', function() {
      return browser
        .getTitle().should.eventually.contain('How are you feeling?? - Multiple Question Title Test')
        .click(DefaultTitlePage.good())
        .click(DefaultTitlePage.submit())
        .getTitle().should.eventually.contain('Who are you answering on behalf of? - Multiple Question Title Test')
        .click(SingleTitlePage.chad())
        .click(SingleTitlePage.submit())
        .getTitle().should.eventually.contain('What is … gender? - Multiple Question Title Test')
        .click(ConditionalTitlePage.genderMale())
        .setValue(ConditionalTitlePage.age(), '25')
        .click(ConditionalTitlePage.sureYes())
        .click(SingleTitlePage.submit())
        .getTitle().should.eventually.contain('Summary - Multiple Question Title Test');
    });
  });



  describe('Given I start the different version of question titles survey', function() {
    beforeEach(function() {
      return browser
        .click(DefaultTitlePage.good())
        .click(DefaultTitlePage.submit());
  });
    it('When I navigate to the proxy question and select Chad, Then I should see versions of questions aimed at Chad on the next page', function() {
      return browser
        .click(SingleTitlePage.chad())
        .click(SingleTitlePage.submit())
        .getText(ConditionalTitlePage.questionText()).should.eventually.contain('What is chad’s gender?')
        .getText(ConditionalTitlePage.questionText()).should.eventually.contain('What is chad’s age?');
    });

    it('When I navigate to the proxy question and select Kelly, Then I should see versions of questions aimed at Kelly on the next page', function() {
      return browser
        .click(SingleTitlePage.kelly())
        .click(SingleTitlePage.submit())
        .getText(ConditionalTitlePage.questionText()).should.eventually.contain('What is kelly’s gender?')
        .getText(ConditionalTitlePage.questionText()).should.eventually.contain('What is kelly’s age?');
    });

    it('When I navigate to the proxy question and select Someone else, Then I should see versions of questions aimed at a 3rd person on the next page', function() {
      return browser
        .click(SingleTitlePage.else())
        .click(SingleTitlePage.submit())
        .getText(ConditionalTitlePage.questionText()).should.eventually.contain('What is their gender?')
        .getText(ConditionalTitlePage.questionText()).should.eventually.contain('What is their age?');
    });

    it('When I navigate to the proxy question and select myself, Then I should see versions of questions aimed at myself on the next page', function() {
      return browser
        .click(SingleTitlePage.myself())
        .click(SingleTitlePage.submit())
        .getText(ConditionalTitlePage.questionText()).should.eventually.contain('What is your gender?')
        .getText(ConditionalTitlePage.questionText()).should.eventually.contain('What is your age?');
    });
  });

  describe('Given I start the different version of question titles survey', function() {
    it('When I navigate to the summary having selected a default title, and single title and a condition title, Then I should see correct question titles rendered on the summary page', function() {
      return browser
        .click(DefaultTitlePage.good())
        .click(DefaultTitlePage.submit())
        .click(SingleTitlePage.chad())
        .click(SingleTitlePage.submit())
        .click(ConditionalTitlePage.genderMale())
        .setValue(ConditionalTitlePage.age(), '25')
        .click(ConditionalTitlePage.sureYes())
        .click(SingleTitlePage.submit())
        .getText(SummaryPage.summaryQuestionText()).should.eventually.contain('How are you feeling??')
        .getText(SummaryPage.summaryQuestionText()).should.eventually.contain('Who are you answering on behalf of?')
        .getText(SummaryPage.summaryQuestionText()).should.eventually.contain('What is chad’s gender?')
        .getText(SummaryPage.summaryQuestionText()).should.eventually.contain('What is chad’s age?');
    });
  });
});
