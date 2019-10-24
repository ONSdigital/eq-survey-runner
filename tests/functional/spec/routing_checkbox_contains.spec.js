const helpers = require('../helpers');
const RoutingCheckboxContains = require('../generated_pages/routing_checkbox_contains/country-checkbox.page');
const ContainsAllPage = require('../generated_pages/routing_checkbox_contains/country-interstitial-all.page');
const ContainsAnyPage = require('../generated_pages/routing_checkbox_contains/country-interstitial-any.page');
const ResponseSummaryPage = require('../generated_pages/routing_checkbox_contains/summary.page');

describe('Routing Checkbox Contains Condition.', function () {
  let browser;

  beforeEach(function () {
    helpers.openQuestionnaire('test_routing_checkbox_contains.json').then(openBrowser => browser = openBrowser);
  });

  it('Given a list of checkbox options, when I have don\'t select "Liechtenstein" and select the option "India" or the option "Azerbaijan" or both then I should be routed to the "contains any" condition page', function () {
    // When
    expect($(RoutingCheckboxContains.liechtenstein()).isSelected()).to.be.false;

    $(RoutingCheckboxContains.india()).click();
    $(RoutingCheckboxContains.submit()).click();
    // Then
    expect(browser.getUrl()).to.contain(ContainsAnyPage.pageName);

    // Or
    $(ContainsAnyPage.previous()).click();

    // When
    $(RoutingCheckboxContains.india()).click();
    $(RoutingCheckboxContains.azerbaijan()).click();
    $(RoutingCheckboxContains.submit()).click();

    // Then
    expect(browser.getUrl()).to.contain(ContainsAnyPage.pageName);

    // Or
    $(ContainsAnyPage.previous()).click();

    // When
    $(RoutingCheckboxContains.india()).click();
    $(RoutingCheckboxContains.submit()).click();

    // Then
    expect(browser.getUrl()).to.contain(ContainsAnyPage.pageName);
  });

  it('Given a list of checkbox options, when I select the option "Malta" or the option "Liechtenstein" or both then I should be routed to the summary condition page', function () {
    //Given
      // When
      $(RoutingCheckboxContains.liechtenstein()).click();
      $(RoutingCheckboxContains.submit()).click();
      // Then
      expect(browser.getUrl()).to.contain(ResponseSummaryPage.pageName);

      // Or
      $(ContainsAnyPage.previous()).click();

      // When
      $(RoutingCheckboxContains.liechtenstein()).click();
      $(RoutingCheckboxContains.malta()).click();
      $(RoutingCheckboxContains.submit()).click();

      // Then
      expect(browser.getUrl()).to.contain(ResponseSummaryPage.pageName);

      // Or
      $(ContainsAnyPage.previous()).click();

      // When
      $(RoutingCheckboxContains.liechtenstein()).click();
      $(RoutingCheckboxContains.submit()).click();

      // Then
      expect(browser.getUrl()).to.contain(ResponseSummaryPage.pageName);

  });

  it('Given a list of checkbox options, when I select the options "India", "Azerbaijan" and "Liechtenstein" then I should be routed to the "contains all" condition page', function () {
    //Given
      //When
      $(RoutingCheckboxContains.india()).click();
      $(RoutingCheckboxContains.azerbaijan()).click();
      $(RoutingCheckboxContains.liechtenstein()).click();
      $(RoutingCheckboxContains.submit()).click();
      // Then
      expect(browser.getUrl()).to.contain(ContainsAllPage.pageName);
  });

});
