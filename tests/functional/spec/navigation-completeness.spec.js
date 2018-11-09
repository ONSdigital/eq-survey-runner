const helpers = require('../helpers');
const CoffeePage = require('../generated_pages/navigation_completeness/coffee.page.js');
const ResponseYesPage = require('../generated_pages/navigation_completeness/response-yes.page.js');
const ResponseNoPage = require('../generated_pages/navigation_completeness/response-no.page.js');

describe('Completeness', function() {

  before("Launch Survey", function () {
    return helpers.openQuestionnaire('test_navigation_completeness.json');
  });

  it("When I complete a section then it should be marked complete", function () {
    return browser
      .click(CoffeePage.yes())
      .click(CoffeePage.submit())
      .setValue(ResponseYesPage.numberOfCups(), 2)
      .click(ResponseYesPage.submit())
      .then(helpers.isSectionComplete('Coffee')).should.eventually.be.true;
  });

  it("When I go back and change the routing path the section should be marked as incomplete", function () {
    return browser
      .click(helpers.navigationLink("Coffee"))
      .click(CoffeePage.no())
      .click(CoffeePage.submit())
      .then(helpers.isSectionComplete('Coffee')).should.eventually.be.false;
  });

  it("When I complete the new path, then the section is marked as complete", function () {
    return browser
      .setValue(ResponseNoPage.numberOfCups(), 5)
      .click(ResponseNoPage.submit())
      .then(helpers.isSectionComplete('Coffee')).should.eventually.be.true;
  });
});

