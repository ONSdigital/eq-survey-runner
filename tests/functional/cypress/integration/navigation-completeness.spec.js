import {openQuestionnaire} from '../helpers/helpers.js';
const CoffeePage = require('../../generated_pages/navigation_completeness/coffee.page.js');
const ResponseYesPage = require('../../generated_pages/navigation_completeness/response-yes.page.js');
const ResponseNoPage = require('../../generated_pages/navigation_completeness/response-no.page.js');

describe('Completeness', function() {

  beforeEach(() => {
    openQuestionnaire('test_navigation_completeness.json');
  });

  it('When I complete a section then it should be marked complete', function() {
    cy
      .get(CoffeePage.yes()).click()
      .get(CoffeePage.submit()).click()
      .get(ResponseYesPage.numberOfCups()).type(2)
      .get(ResponseYesPage.submit()).click()
      .isSectionComplete('Coffee').should('be.true');
  });

  it('When I go back and change the routing path the section should be marked as incomplete', function() {
    cy
      .navigationLink('Coffee').click()
      .get(CoffeePage.no()).click()
      .get(CoffeePage.submit()).click()
      .isSectionComplete('Coffee').should('be.false');
  });

  it('When I complete the new path, then the section is marked as complete', function() {
    cy
      .get(CoffeePage.no()).click()
      .get(CoffeePage.submit()).click()
      .get(ResponseNoPage.numberOfCups()).type(5)
      .get(ResponseNoPage.submit()).click()
      .isSectionComplete('Coffee').should('be.true');
  });
});

