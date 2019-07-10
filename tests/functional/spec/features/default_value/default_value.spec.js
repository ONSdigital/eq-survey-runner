const helpers = require('../../../helpers');

const QuestionPageOne = require('../../../generated_pages/default/number-question-one.page.js');
const QuestionPageTwo = require('../../../generated_pages/default/number-question-two.page.js');
const Summary = require('../../../generated_pages/default/summary.page.js');
const QuestionPageOneSkip = require('../../../generated_pages/default_with_skip/number-question-one.page.js');
const QuestionPageThreeSkip = require('../../../generated_pages/default_with_skip/number-question-three.page.js');


describe('Feature: Default Value', function() {

  it('Given I start default schema, When I do not answer a question, Then "no answer provided" is displayed on the Summary page', function() {
    return helpers.openQuestionnaire('test_default.json').then(() => {
      return browser
        .click(QuestionPageOne.submit())
          .getUrl().should.eventually.contain(QuestionPageTwo.pageName)
          .setValue(QuestionPageTwo.two(), 123)
          .click(QuestionPageTwo.submit())
          .getUrl().should.eventually.contain(Summary.pageName)
          .getText(Summary.answerOne()).should.eventually.contain('No answer provided');
    });
  });

  it('Given I have not answered a question containing a default value, When I return to the question, Then no value should be displayed', function() {
  return helpers.openQuestionnaire('test_default.json').then(() => {
    return browser
      .click(QuestionPageOne.submit())
        .getUrl().should.eventually.contain(QuestionPageTwo.pageName)
        .setValue(QuestionPageTwo.two(), 123)
        .click(QuestionPageTwo.submit())
        .getUrl().should.eventually.contain(Summary.pageName)
        .click(Summary.previous())
        .getUrl().should.eventually.contain(QuestionPageTwo.pageName)
        .click(QuestionPageTwo.previous())
        .getUrl().should.eventually.contain(QuestionPageOne.pageName)
        .getValue(QuestionPageOne.one()).should.eventually.equal('');
    });
  });

  it('Given I have not answered a question containing a default value, When a skip condition checks for the default value, Then I should skip the next question', function() {
  return helpers.openQuestionnaire('test_default_with_skip.json').then(() => {
    return browser
      .click(QuestionPageOneSkip.submit())
       .getUrl().should.eventually.contain(QuestionPageThreeSkip.pageName)
       .getText(QuestionPageThreeSkip.questionText()).should.eventually.contain('Question Three');
    });
   });
});
