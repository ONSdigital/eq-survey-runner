import {openQuestionnaire} from '../../../helpers/helpers.js';

const RouteComparison1Page = require('../../../../generated_pages/routing_answer_comparison/route-comparison-1.page.js');
const RouteComparison2Page = require('../../../../generated_pages/routing_answer_comparison/route-comparison-2.page.js');
const RouteComparison3Page = require('../../../../generated_pages/routing_answer_comparison/route-comparison-3.page.js');
const RouteComparison4Page = require('../../../../generated_pages/routing_answer_comparison/route-comparison-4.page.js');

describe('Test routing skip', function() {

  beforeEach(function() {
    openQuestionnaire('test_routing_answer_comparison.json');
  });

  it('Given we start the routing test survey, When we enter a low number then a high number, Then, we should be routed to the fourth page', function() {
    cy
      .get(RouteComparison1Page.answer()).type(1)
      .get(RouteComparison1Page.submit()).click()
      .get(RouteComparison2Page.answer()).type(2)
      .get(RouteComparison2Page.submit()).click()
      .get(RouteComparison4Page.interstitialHeader()).stripText().should('contain', 'Your second number was higher');
  });

  it('Given we start the routing test survey, When we enter a high number then a low number, Then, we should be routed to the third page', function() {
    cy
      .get(RouteComparison1Page.answer()).type(1)
      .get(RouteComparison1Page.submit()).click()
      .get(RouteComparison2Page.answer()).type(0)
      .get(RouteComparison2Page.submit()).click()
      .get(RouteComparison3Page.interstitialHeader()).stripText().should('contain', 'Your second number was lower or equal');
  });

  it('Given we start the routing test survey, When we enter an equal number on both questions, Then, we should be routed to the third page', function() {
    cy
      .get(RouteComparison1Page.answer()).type(1)
      .get(RouteComparison1Page.submit()).click()
      .get(RouteComparison2Page.answer()).type(1)
      .get(RouteComparison2Page.submit()).click()
      .get(RouteComparison3Page.interstitialHeader()).stripText().should('contain', 'Your second number was lower or equal');
  });
});

