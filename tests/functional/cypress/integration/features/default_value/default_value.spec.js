import {openQuestionnaire} from ../../../helpers/helpers.js

const QuestionPage = require('../../../generated_pages/default/number-question.page.js');
const Summary = require('../../../generated_pages/default/summary.page.js');

describe('Feature: Default Value', function() {

  it('Given I start default schema, When I do not give a value, Then the default value will be stored', function() {
    openQuestionnaire('test_default.json')
              .get(QuestionPage.submit()).click()
          .url().should('contain', Summary.pageName)
          .get(Summary.answer()).stripText().should('contain', '0')
          .get(Summary.previous()).click()
          .url().should('contain', QuestionPage.pageName)
          .get(QuestionPage.answer()).invoke('val').should('contain', '0');
    });
  });
});
