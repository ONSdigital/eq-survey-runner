const helpers = require('../helpers');
const RoutingCheckboxContains = require('../generated_pages/routing_checkbox_contains/country-checkbox.page');
const ContainsAllPage = require('../generated_pages/routing_checkbox_contains/country-interstitial-all.page');
const ContainsAnyPage = require('../generated_pages/routing_checkbox_contains/country-interstitial-any.page');
const ResponseSummaryPage = require('../generated_pages/routing_checkbox_contains/summary.page');

describe('Routing Checkbox Contains Condition.', function () {

  beforeEach(function () {
    return helpers.openQuestionnaire('test_routing_checkbox_contains.json');
  });

  it('Given a list of checkbox options, when I have don\'t select "Liechtenstein" and select the option "India" or the option "Azerbaijan" or both then I should be routed to the "contains any" condition page', function () {
    //Given
    return browser
      // When
      .isSelected(RoutingCheckboxContains.liechtenstein()).should.eventually.be.false

      .click(RoutingCheckboxContains.india())
      .click(RoutingCheckboxContains.submit())
      // Then
      .getUrl().should.eventually.contain(ContainsAnyPage.pageName)

      // Or
      .click(ContainsAnyPage.previous())

      // When
      .click(RoutingCheckboxContains.india())
      .click(RoutingCheckboxContains.azerbaijan())
      .click(RoutingCheckboxContains.submit())

      // Then
      .getUrl().should.eventually.contain(ContainsAnyPage.pageName)

      // Or
      .click(ContainsAnyPage.previous())

      // When
      .click(RoutingCheckboxContains.india())
      .click(RoutingCheckboxContains.submit())

      // Then
      .getUrl().should.eventually.contain(ContainsAnyPage.pageName);

  });

  it('Given a list of checkbox options, when I select the option "Malta" or the option "Liechtenstein" or both then I should be routed to the summary condition page', function () {
    //Given
    return browser
      // When
      .click(RoutingCheckboxContains.liechtenstein())
      .click(RoutingCheckboxContains.submit())
      // Then
      .getUrl().should.eventually.contain(ResponseSummaryPage.pageName)

      // Or
      .click(ContainsAnyPage.previous())

      // When
      .click(RoutingCheckboxContains.liechtenstein())
      .click(RoutingCheckboxContains.malta())
      .click(RoutingCheckboxContains.submit())

      // Then
      .getUrl().should.eventually.contain(ResponseSummaryPage.pageName)

      // Or
      .click(ContainsAnyPage.previous())

      // When
      .click(RoutingCheckboxContains.liechtenstein())
      .click(RoutingCheckboxContains.submit())

      // Then
      .getUrl().should.eventually.contain(ResponseSummaryPage.pageName);

  });

  it('Given a list of checkbox options, when I select the options "India", "Azerbaijan" and "Liechtenstein" then I should be routed to the "contains all" condition page', function () {
    //Given
    return browser
      //When
      .click(RoutingCheckboxContains.india())
      .click(RoutingCheckboxContains.azerbaijan())
      .click(RoutingCheckboxContains.liechtenstein())
      .click(RoutingCheckboxContains.submit())
      // Then
      .getUrl().should.eventually.contain(ContainsAllPage.pageName);
  });

});
