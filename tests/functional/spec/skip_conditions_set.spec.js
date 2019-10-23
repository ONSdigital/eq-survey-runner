const helpers = require('../helpers');
const FoodPage = require('../generated_pages/skip_condition_set/food-block.page');
const DrinkPage = require('../generated_pages/skip_condition_set/drink-block.page');
const SummaryPage = require('../generated_pages/skip_condition_set/summary.page');

describe('Skip Conditions - Set', function() {
  let browser;

  beforeEach('Load the survey', function () {
    browser = helpers.openQuestionnaire('test_skip_condition_set.json').then(openBrowser => browser = openBrowser);
  });

  it('Given I complete the first page, Then I should see the summary page', function() {
    $(FoodPage.bacon()).click();
    $(FoodPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  });

  it('Given I do not complete the first page, Then I should see the drink page', function() {
    $(FoodPage.submit()).click();
    expect(browser.getUrl()).to.contain(DrinkPage.pageName);
  });
});
