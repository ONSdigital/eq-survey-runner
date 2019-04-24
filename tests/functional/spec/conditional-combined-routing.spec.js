const helpers = require('../helpers');
const ConditionalCombinedRoutingPage = require('../generated_pages/conditional_combined_routing/conditional-routing-block.page');
const ResponseAny = require('../generated_pages/conditional_combined_routing/response-any.page');
const ResponseNotAny = require('../generated_pages/conditional_combined_routing/response-not-any.page');
const ResponseSummaryPage = require('../generated_pages/conditional_combined_routing/summary.page');

describe('Conditional combined routing.', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_conditional_combined_routing.json');
  });

  it('Given a list of radio options, when I choose the option "Yes" or the option "Sometimes" then I should be routed to the relevant page', function() {
    //Given
    return browser
      // When
      .click(ConditionalCombinedRoutingPage.yes())
      .click(ConditionalCombinedRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(ResponseAny.pageName)

      // Or
      .click(ResponseAny.previous())

      // When
      .click(ConditionalCombinedRoutingPage.sometimes())
      .click(ConditionalCombinedRoutingPage.submit())

      // Then
      .getUrl().should.eventually.contain(ResponseAny.pageName);

  });

  it('Given a list of radio options, when I choose the option "No, I prefer tea" then I should be routed to the relevant page', function() {
    //Given
    return browser
      //When
      .click(ConditionalCombinedRoutingPage.noIPreferTea())
      .click(ConditionalCombinedRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(ResponseNotAny.pageName);
  });

  it('Given a list of radio options, when I choose the option "No, I don\'t drink any hot drinks" then I should be routed to the summary page', function() {
    //Given
    return browser
      //When
      .click(ConditionalCombinedRoutingPage.noIDonTDrinkAnyHotDrinks())
      .click(ConditionalCombinedRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(ResponseSummaryPage.pageName);
  });

});
