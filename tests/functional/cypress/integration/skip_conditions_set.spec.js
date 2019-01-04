import {openQuestionnaire} from '../helpers/helpers.js';
const FoodPage = require('../../generated_pages/skip_condition_set/food-block.page');
const DrinkPage = require('../../generated_pages/skip_condition_set/drink-block.page');
const SummaryPage = require('../../generated_pages/skip_condition_set/summary.page');

describe('Skip Conditions - Set', function() {
  beforeEach(() => {
    openQuestionnaire('test_skip_condition_set.json');
  });

  it('Given I complete the first page, Then I should see the summary page', function() {
    cy
      .get(FoodPage.bacon()).click()
      .get(FoodPage.submit()).click()
      .url().should('contain', SummaryPage.pageName);
  });

  it('Given I do not complete the first page, Then I should see the drink page', function() {
    cy
      .get(FoodPage.submit()).click()
      .url().should('contain', DrinkPage.pageName);
  });
});
