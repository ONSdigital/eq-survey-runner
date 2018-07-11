const helpers = require('../helpers');
const FoodPage = require('../pages/surveys/skip_conditions_set/food-block.page');
const SummaryPage = require('../pages/surveys/skip_conditions_set/summary.page');

describe('Skip Conditions - Set', function() {
  it('Given I am skipping the middle page. When I complete the first page, Then I should see the summary page', function() {
    return helpers.openQuestionnaire('test_skip_condition_set.json').then(() => {
      return browser
        .click(FoodPage.bacon())
        .click(FoodPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });
});
