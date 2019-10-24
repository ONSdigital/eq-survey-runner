const helpers = require('../../../helpers');

const ToppingCheckboxPage =           require('../../../generated_pages/routing_checkbox_set_not_set/topping-checkbox.page.js');
const ToppingInterstitialNotSetPage = require('../../../generated_pages/routing_checkbox_set_not_set/topping-interstitial-not-set.page.js');
const ToppingInterstitialSetPage =    require('../../../generated_pages/routing_checkbox_set_not_set/topping-interstitial-set.page.js');
const OptionalMutuallyExclusivePage = require('../../../generated_pages/routing_checkbox_set_not_set/optional-mutually-exclusive.page.js');
const CheeseInterstitialNotSetPage =  require('../../../generated_pages/routing_checkbox_set_not_set/cheese-interstitial-not-set.page.js');
const CheeseInterstitialSetPage =     require('../../../generated_pages/routing_checkbox_set_not_set/cheese-interstitial-set.page.js');
const SummaryPage =                   require('../../../generated_pages/routing_checkbox_set_not_set/summary.page.js');

describe('Test routing using not set and set conditions on checkboxes', function() {
  let browser;

  beforeEach(function() {
    helpers.openQuestionnaire('test_routing_checkbox_set_not_set.json').then(openBrowser => browser = openBrowser);
  });

  it('Given a user sets a topping and a cheese, they should see an interstitial for each saying that they were set', function() {
    $(ToppingCheckboxPage.cheese()).click();
    $(ToppingCheckboxPage.submit()).click();

    expect(browser.getUrl()).to.contain(ToppingInterstitialSetPage.pageName);

    $(ToppingInterstitialSetPage.submit()).click();

    $(OptionalMutuallyExclusivePage.noCheese()).click();
    $(OptionalMutuallyExclusivePage.submit()).click();

    expect(browser.getUrl()).to.contain(CheeseInterstitialSetPage.pageName);

    $(CheeseInterstitialSetPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  });

  it('Given a user does not set a topping and does not set a cheese, they should see an interstitial for each saying that they were not set', function() {
    $(ToppingCheckboxPage.submit()).click();

    expect(browser.getUrl()).to.contain(ToppingInterstitialNotSetPage.pageName);

    $(ToppingInterstitialNotSetPage.submit()).click();

    $(OptionalMutuallyExclusivePage.submit()).click();

    expect(browser.getUrl()).to.contain(CheeseInterstitialNotSetPage.pageName);

    $(CheeseInterstitialNotSetPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  });
});

