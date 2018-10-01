const helpers = require('../../../helpers');

const ToppingCheckboxPage = require('../../../pages/features/routing/set_not_set/checkbox/topping-checkbox.page.js');
const ToppingInterstitialNotSetPage = require('../../../pages/features/routing/set_not_set/checkbox/topping-interstitial-not-set.page.js');
const ToppingInterstitialSetPage = require('../../../pages/features/routing/set_not_set/checkbox/topping-interstitial-set.page.js');
const OptionalMutuallyExclusivePage = require('../../../pages/features/routing/set_not_set/checkbox/optional-mutually-exclusive.page.js');
const CheeseInterstitialNotSetPage = require('../../../pages/features/routing/set_not_set/checkbox/cheese-interstitial-not-set.page.js');
const CheeseInterstitialSetPage = require('../../../pages/features/routing/set_not_set/checkbox/cheese-interstitial-set.page.js');
const SummaryPage = require('../../../pages/features/routing/set_not_set/checkbox/summary.page.js');

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

