const helpers = require('../../../helpers');

const RouteComparison1Page = require('../../../generated_pages/routing_answer_comparison/route-comparison-1.page.js');
const RouteComparison2Page = require('../../../generated_pages/routing_answer_comparison/route-comparison-2.page.js');
const RouteComparison3Page = require('../../../generated_pages/routing_answer_comparison/route-comparison-3.page.js');
const RouteComparison4Page = require('../../../generated_pages/routing_answer_comparison/route-comparison-4.page.js');

describe('Test routing skip', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_routing_answer_comparison.json');
  });

  it('Given we start the routing test survey, When we enter a low number then a high number, Then, we should be routed to the fourth page', function() {
    return browser
      .setValue(RouteComparison1Page.answer(), 1)
      .click(RouteComparison1Page.submit())
      .setValue(RouteComparison2Page.answer(), 2)
      .click(RouteComparison2Page.submit())
      .getText(RouteComparison4Page.interstitialHeader()).should.eventually.contain('Your second number was higher');
    });

  it('Given we start the routing test survey, When we enter a high number then a low number, Then, we should be routed to the third page', function() {
    return browser
      .setValue(RouteComparison1Page.answer(), 1)
      .click(RouteComparison1Page.submit())
      .setValue(RouteComparison2Page.answer(), 0)
      .click(RouteComparison2Page.submit())
      .getText(RouteComparison3Page.interstitialHeader()).should.eventually.contain('Your second number was lower or equal');
    });

  it('Given we start the routing test survey, When we enter an equal number on both questions, Then, we should be routed to the third page', function() {
    return browser
      .setValue(RouteComparison1Page.answer(), 1)
      .click(RouteComparison1Page.submit())
      .setValue(RouteComparison2Page.answer(), 1)
      .click(RouteComparison2Page.submit())
      .getText(RouteComparison3Page.interstitialHeader()).should.eventually.contain('Your second number was lower or equal');
    });
});

