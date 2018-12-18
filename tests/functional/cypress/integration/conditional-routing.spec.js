import {openQuestionnaire} from '../helpers/helpers.js'

const ConditionalRoutingPage = require('../../generated_pages/conditional_routing/conditional-routing-block.page');
const ResponseYesPage = require('../../generated_pages/conditional_routing/response-yes.page');
const ResponseNoPage = require('../../generated_pages/conditional_routing/response-no.page');

describe('Conditional routing.', function () {

  var basic_yes_no_question_schema = 'test_conditional_routing.json';

  beforeEach(function () {
    openQuestionnaire(basic_yes_no_question_schema)
  })

  it('Given a yes no question, when I select yes, I should be routed to the Yes response page.', function () {
    cy
      .get(ConditionalRoutingPage.yes()).click()
      .get(ConditionalRoutingPage.submit()).click()
      .url().should('contain', ResponseYesPage.pageName);
  });

  it('Given a yes no question, when I select no, I should be routed to the No response page.', function () {
    cy
      .get(ConditionalRoutingPage.no()).click()
      .get(ConditionalRoutingPage.submit()).click()
      .url().should('contain', ResponseNoPage.pageName);
  });
});
