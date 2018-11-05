const helpers = require('../../../helpers');

const QuestionPage = require('../../../generated_pages/default/number-question.page.js');
const Summary = require('../../../generated_pages/default/summary.page.js');

describe('Feature: Default Value', function() {

  it('Given I start default schema, When I do not give a value, Then the default value will be stored', function() {
    return helpers.openQuestionnaire('test_default.json').then(() => {
      return browser
        .click(QuestionPage.submit())
          .getUrl().should.eventually.contain(Summary.pageName)
          .getText(Summary.answer()).should.eventually.contain('0')
          .click(Summary.previous())
          .getUrl().should.eventually.contain(QuestionPage.pageName)
          .getValue(QuestionPage.answer()).should.eventually.contain('0');
    });
  });
});
