const helpers = require('../helpers');
const FoodPage = require('../generated_pages/skip_condition_set/food-block.page');
const DrinkPage = require('../generated_pages/skip_condition_set/drink-block.page');
const SummaryPage = require('../generated_pages/skip_condition_set/summary.page');

describe('Skip Conditions - Set', function() {
  it('Given I complete the first page, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_set.json').then(() => {
      return browser
        .click(FoodPage.bacon())
        .click(FoodPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

  it('Given I do not complete the first page, Then I should see the drink page', function() {
    return helpers.openQuestionnaire('test_skip_condition_set.json').then(() => {
      return browser
        .click(FoodPage.submit())
        .getUrl().should.eventually.contain(DrinkPage.pageName);
    });
  });
});
