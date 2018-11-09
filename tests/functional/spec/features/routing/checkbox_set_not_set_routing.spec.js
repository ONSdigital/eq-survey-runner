const helpers = require('../../../helpers');

const ToppingCheckboxPage =           require('../../../generated_pages/routing_checkbox_set_not_set/topping-checkbox.page.js');
const ToppingInterstitialNotSetPage = require('../../../generated_pages/routing_checkbox_set_not_set/topping-interstitial-not-set.page.js');
const ToppingInterstitialSetPage =    require('../../../generated_pages/routing_checkbox_set_not_set/topping-interstitial-set.page.js');
const OptionalMutuallyExclusivePage = require('../../../generated_pages/routing_checkbox_set_not_set/optional-mutually-exclusive.page.js');
const CheeseInterstitialNotSetPage =  require('../../../generated_pages/routing_checkbox_set_not_set/cheese-interstitial-not-set.page.js');
const CheeseInterstitialSetPage =     require('../../../generated_pages/routing_checkbox_set_not_set/cheese-interstitial-set.page.js');
const SummaryPage =                   require('../../../generated_pages/routing_checkbox_set_not_set/summary.page.js');

describe('Test routing using not set and set conditions on checkboxes', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_routing_checkbox_set_not_set.json');
  });

  it('Given a user sets a topping and a cheese, they should see an interstitial for each saying that they were set', function() {
      return browser
        .click(ToppingCheckboxPage.cheese())
        .click(ToppingCheckboxPage.submit())

        .getUrl().should.eventually.contain(ToppingInterstitialSetPage.pageName)

        .click(ToppingInterstitialSetPage.submit())

        .click(OptionalMutuallyExclusivePage.noCheese())
        .click(OptionalMutuallyExclusivePage.submit())

        .getUrl().should.eventually.contain(CheeseInterstitialSetPage.pageName)

        .click(CheeseInterstitialSetPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName);
  });

  it('Given a user does not set a topping and does not set a cheese, they should see an interstitial for each saying that they were not set', function() {
      return browser
        .click(ToppingCheckboxPage.submit())

        .getUrl().should.eventually.contain(ToppingInterstitialNotSetPage.pageName)

        .click(ToppingInterstitialNotSetPage.submit())

        .click(OptionalMutuallyExclusivePage.submit())

        .getUrl().should.eventually.contain(CheeseInterstitialNotSetPage.pageName)

        .click(CheeseInterstitialNotSetPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName);
  });
});

