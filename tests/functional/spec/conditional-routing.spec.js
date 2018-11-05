const helpers = require('../helpers');
const ConditionalRoutingPage = require('../generated_pages/conditional_routing/conditional-routing-block.page');
const ResponseYesPage = require('../generated_pages/conditional_routing/response-yes.page');
const ResponseNoPage = require('../generated_pages/conditional_routing/response-no.page');

describe('Conditional routing.', function() {

  var basic_yes_no_question_schema = 'test_conditional_routing.json';

  it('Given a yes no question, when I select yes, I should be routed to the Yes response page.', function() {
    //Given
    return helpers.openQuestionnaire(basic_yes_no_question_schema).then(() => {
      return browser
      // When
        .click(ConditionalRoutingPage.yes())
        .click(ConditionalRoutingPage.submit())
      // Then
        .getUrl().should.eventually.contain(ResponseYesPage.pageName);
    });
  });

  it('Given a yes no question, when I select no, I should be routed to the No response page.', function() {
    //Given
    return helpers.openQuestionnaire(basic_yes_no_question_schema).then(() => {
      return browser
      //When
        .click(ConditionalRoutingPage.no())
        .click(ConditionalRoutingPage.submit())
      // Then
        .getUrl().should.eventually.contain(ResponseNoPage.pageName);
    });

  });
});
