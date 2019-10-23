const helpers = require('../../../helpers');

const QuestionPageOne = require('../../../generated_pages/default/number-question-one.page.js');
const QuestionPageTwo = require('../../../generated_pages/default/number-question-two.page.js');
const Summary = require('../../../generated_pages/default/summary.page.js');
const QuestionPageOneSkip = require('../../../generated_pages/default_with_skip/number-question-one.page.js');
const QuestionPageThreeSkip = require('../../../generated_pages/default_with_skip/number-question-three.page.js');


describe('Feature: Default Value', function() {
  let browser;

  it('Given I start default schema, When I do not answer a question, Then "no answer provided" is displayed on the Summary page', function() {
    browser = helpers.openQuestionnaire('test_default.json').then(openBrowser => browser = openBrowser);
        $(QuestionPageOne.submit()).click();
          expect(browser.getUrl()).to.contain(QuestionPageTwo.pageName);
          $(QuestionPageTwo.two()).setValue(123);
          $(QuestionPageTwo.submit()).click();
          expect(browser.getUrl()).to.contain(Summary.pageName);
          expect($(Summary.answerOne()).getText()).to.contain('No answer provided');
  });

  it('Given I have not answered a question containing a default value, When I return to the question, Then no value should be displayed', function() {
  browser = helpers.openQuestionnaire('test_default.json').then(openBrowser => browser = openBrowser);
      $(QuestionPageOne.submit()).click();
        expect(browser.getUrl()).to.contain(QuestionPageTwo.pageName);
        $(QuestionPageTwo.two()).setValue(123);
        $(QuestionPageTwo.submit()).click();
        expect(browser.getUrl()).to.contain(Summary.pageName);
        $(Summary.previous()).click();
        expect(browser.getUrl()).to.contain(QuestionPageTwo.pageName);
        $(QuestionPageTwo.previous()).click();
        expect(browser.getUrl()).to.contain(QuestionPageOne.pageName);
        $(QuestionPageOne.one()).getValue();
  });

  it('Given I have not answered a question containing a default value, When a skip condition checks for the default value, Then I should skip the next question', function() {
  browser = helpers.openQuestionnaire('test_default_with_skip.json').then(openBrowser => browser = openBrowser);
      $(QuestionPageOneSkip.submit()).click();
       expect(browser.getUrl()).to.contain(QuestionPageThreeSkip.pageName);
       expect($(QuestionPageThreeSkip.questionText()).getText()).to.contain('Question Three');
   });
});
