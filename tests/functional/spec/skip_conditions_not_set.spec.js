const helpers = require('../helpers');
const FoodPage = require('../pages/surveys/skip_conditions_not_set/food-block.page');
const DrinkPage = require('../pages/surveys/skip_conditions_not_set/drink-block.page');
const SummaryPage = require('../pages/surveys/skip_conditions_not_set/summary.page');

describe('Skip Conditions - Not Set', function() {
  it('Given I am skipping the middle page. When I do not provide an answer on the first page, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_not_set.json').then(() => {
      return browser
        .click(FoodPage.bacon())
        .click(FoodPage.submit())
        .click(DrinkPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });
});
