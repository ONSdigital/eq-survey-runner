const helpers = require('../helpers');
const PositiveRoutingPage = require('../generated_pages/routing_values_array/block-one.page');
const AllAnyOfConditionTrue = require('../generated_pages/routing_values_array/block-two.page');
const NotAllOfRoutingPage = require('../generated_pages/routing_values_array/block-four.page');
const NotAllOfConditionTrue = require('../generated_pages/routing_values_array/block-five.page');
const NotAnyOfRoutingPage = require('../generated_pages/routing_values_array/block-six.page');
const NotAnyOfConditionTrue = require('../generated_pages/routing_values_array/block-seven.page');

describe('Conditional combined routing.', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_routing_values_array.json');
  });

  it('Given the contains all routing rule when I fulfil it I should go to the right page ', function() {
    //Given
    return browser
      // When
      .click(PositiveRoutingPage.box1())
      .click(PositiveRoutingPage.box2())
      .click(PositiveRoutingPage.box3())
      .click(PositiveRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(AllAnyOfConditionTrue.pageName)
      // Or 
      .click(AllAnyOfConditionTrue.previous())
      .click(PositiveRoutingPage.box4())
      .click(PositiveRoutingPage.submit())
      .getUrl().should.eventually.contain(AllAnyOfConditionTrue.pageName);

  });

  it('Given the contains any of routing rule when I fulfil it I should go to the right page ', function() {
    //Given
    return browser
      // When
      .click(PositiveRoutingPage.box1())
      .click(PositiveRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(AllAnyOfConditionTrue.pageName)
      // Or 
      .click(AllAnyOfConditionTrue.previous())
      .click(PositiveRoutingPage.box2())
      .click(PositiveRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(AllAnyOfConditionTrue.pageName)
      // Or 
      .click(AllAnyOfConditionTrue.previous())
      .click(PositiveRoutingPage.box2())
      .click(PositiveRoutingPage.box3())
      .click(PositiveRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(AllAnyOfConditionTrue.pageName);


  });

  it('Given the not contains all routing rule when I fulfil it I should go to the right page ', function() {
    //Given
    return browser
      // When
      .click(PositiveRoutingPage.submit())
      .getUrl().should.eventually.contain(NotAllOfRoutingPage.pageName)
      .click(NotAllOfRoutingPage.box1())
      .click(NotAllOfRoutingPage.box2())
      .click(NotAllOfRoutingPage.box4())
      .click(NotAllOfRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(NotAllOfConditionTrue.pageName)
      //Or
      .click(NotAllOfConditionTrue.previous())
      .click(NotAllOfRoutingPage.box3())
      .click(NotAllOfRoutingPage.submit())
      // Then
      .getUrl().should.eventually.contain(NotAnyOfRoutingPage.pageName);


  });

  it('Given the not contains any routing rule when I fulfil it I should go to the right page ', function() {
    //Given
    return browser
    .click(PositiveRoutingPage.submit())
    .getUrl().should.eventually.contain(NotAllOfRoutingPage.pageName)
    .click(NotAllOfRoutingPage.box1())
    .click(NotAllOfRoutingPage.box2())
    .click(NotAllOfRoutingPage.box3())
    .click(NotAllOfRoutingPage.submit())
    .getUrl().should.eventually.contain(NotAnyOfRoutingPage.pageName)
    // When
    .click(NotAnyOfRoutingPage.box4())
    .click(NotAnyOfRoutingPage.submit())
    // Then
    .getUrl().should.eventually.contain(NotAnyOfConditionTrue.pageName);

  });

});