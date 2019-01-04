import {openQuestionnaire} from '../../../helpers/helpers.js';

const ToppingCheckboxPage =           require('../../../../generated_pages/routing_checkbox_set_not_set/topping-checkbox.page.js');
const ToppingInterstitialNotSetPage = require('../../../../generated_pages/routing_checkbox_set_not_set/topping-interstitial-not-set.page.js');
const ToppingInterstitialSetPage =    require('../../../../generated_pages/routing_checkbox_set_not_set/topping-interstitial-set.page.js');
const OptionalMutuallyExclusivePage = require('../../../../generated_pages/routing_checkbox_set_not_set/optional-mutually-exclusive.page.js');
const CheeseInterstitialNotSetPage =  require('../../../../generated_pages/routing_checkbox_set_not_set/cheese-interstitial-not-set.page.js');
const CheeseInterstitialSetPage =     require('../../../../generated_pages/routing_checkbox_set_not_set/cheese-interstitial-set.page.js');
const SummaryPage =                   require('../../../../generated_pages/routing_checkbox_set_not_set/summary.page.js');

describe('Test routing using not set and set conditions on checkboxes', function() {

  beforeEach(function() {
    openQuestionnaire('test_routing_checkbox_set_not_set.json');
  });

  it('Given a user sets a topping and a cheese, they should see an interstitial for each saying that they were set', function() {
    cy
      .get(ToppingCheckboxPage.cheese()).click()
      .get(ToppingCheckboxPage.submit()).click()
      .url().should('contain', ToppingInterstitialSetPage.pageName)
      .get(ToppingInterstitialSetPage.submit()).click()
      .get(OptionalMutuallyExclusivePage.noCheese()).click()
      .get(OptionalMutuallyExclusivePage.submit()).click()
      .url().should('contain', CheeseInterstitialSetPage.pageName)
      .get(CheeseInterstitialSetPage.submit()).click()
      .url().should('contain', SummaryPage.pageName);
  });

  it('Given a user does not set a topping and does not set a cheese, they should see an interstitial for each saying that they were not set', function() {
    cy
      .get(ToppingCheckboxPage.submit()).click()
      .url().should('contain', ToppingInterstitialNotSetPage.pageName)
      .get(ToppingInterstitialNotSetPage.submit()).click()
      .get(OptionalMutuallyExclusivePage.submit()).click()
      .url().should('contain', CheeseInterstitialNotSetPage.pageName)
      .get(CheeseInterstitialNotSetPage.submit()).click()
      .url().should('contain', SummaryPage.pageName);
  });
});

