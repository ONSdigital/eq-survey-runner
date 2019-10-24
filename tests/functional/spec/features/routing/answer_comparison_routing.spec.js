const RouteComparison1Page = require('../../../generated_pages/routing_answer_comparison/route-comparison-1.page.js');
const RouteComparison2Page = require('../../../generated_pages/routing_answer_comparison/route-comparison-2.page.js');

describe('Test routing skip', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_routing_answer_comparison.json');
  });

  it('Given we start the routing test survey, When we enter a low number then a high number, Then, we should be routed to the fourth page', function() {
      $(RouteComparison1Page.answer()).setValue(1);
      $(RouteComparison1Page.submit()).click();
      $(RouteComparison2Page.answer()).setValue(2);
      $(RouteComparison2Page.submit()).click();
      expect($('p').getText()).to.contain('This page should never be skipped');
    });

  it('Given we start the routing test survey, When we enter a high number then a low number, Then, we should be routed to the third page', function() {
      $(RouteComparison1Page.answer()).setValue(1);
      $(RouteComparison1Page.submit()).click();
      $(RouteComparison2Page.answer()).setValue(0);
      $(RouteComparison2Page.submit()).click();
      expect($('p').getText()).to.contain('This page should be skipped if your second answer was higher than your first');
    });

  it('Given we start the routing test survey, When we enter an equal number on both questions, Then, we should be routed to the third page', function() {
      $(RouteComparison1Page.answer()).setValue(1);
      $(RouteComparison1Page.submit()).click();
      $(RouteComparison2Page.answer()).setValue(1);
      $(RouteComparison2Page.submit()).click();
      expect($('p').getText()).to.contain('This page should be skipped if your second answer was higher than your first');
    });
});

