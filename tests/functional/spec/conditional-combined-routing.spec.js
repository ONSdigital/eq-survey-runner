const ConditionalCombinedRoutingPage = require('../generated_pages/conditional_combined_routing/conditional-routing-block.page');
const ResponseAny = require('../generated_pages/conditional_combined_routing/response-any.page');
const ResponseNotAny = require('../generated_pages/conditional_combined_routing/response-not-any.page');
const ResponseSummaryPage = require('../generated_pages/conditional_combined_routing/summary.page');

describe('Conditional combined routing.', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_conditional_combined_routing.json');
  });

  it('Given a list of radio options, when I choose the option "Yes" or the option "Sometimes" then I should be routed to the relevant page', function() {
    // When
    $(ConditionalCombinedRoutingPage.yes()).click();
    $(ConditionalCombinedRoutingPage.submit()).click();
    // Then
    expect(browser.getUrl()).to.contain(ResponseAny.pageName);

    // Or
    $(ResponseAny.previous()).click();

    // When
    $(ConditionalCombinedRoutingPage.sometimes()).click();
    $(ConditionalCombinedRoutingPage.submit()).click();

    // Then
    expect(browser.getUrl()).to.contain(ResponseAny.pageName);
  });

  it('Given a list of radio options, when I choose the option "No, I prefer tea" then I should be routed to the relevant page', function() {
    //When
    $(ConditionalCombinedRoutingPage.noIPreferTea()).click();
    $(ConditionalCombinedRoutingPage.submit()).click();
    // Then
    expect(browser.getUrl()).to.contain(ResponseNotAny.pageName);
  });

  it('Given a list of radio options, when I choose the option "No, I don\'t drink any hot drinks" then I should be routed to the summary page', function() {
    //When
    $(ConditionalCombinedRoutingPage.noIDonTDrinkAnyHotDrinks()).click();
    $(ConditionalCombinedRoutingPage.submit()).click();
    // Then
    expect(browser.getUrl()).to.contain(ResponseSummaryPage.pageName);
  });
});
