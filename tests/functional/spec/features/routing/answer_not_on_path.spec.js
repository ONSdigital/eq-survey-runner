const helpers = require('../../../helpers');

const InitialChoicePage =           require('../../../generated_pages/routing_not_affected_by_answers_not_on_path/initial-choice.page.js');
const InvalidPathPage =             require('../../../generated_pages/routing_not_affected_by_answers_not_on_path/invalid-path.page.js');
const InvalidPathInterstitialPage = require('../../../generated_pages/routing_not_affected_by_answers_not_on_path/invalid-path-interstitial.page.js');
const ValidPathPage =               require('../../../generated_pages/routing_not_affected_by_answers_not_on_path/valid-path.page.js');
const ValidFinalInterstitialPage =  require('../../../generated_pages/routing_not_affected_by_answers_not_on_path/valid-final-interstitial.page.js');

describe('Answers not on path are not considered when routing', function() {
  let browser;

  beforeEach(function() {
    browser = helpers.openQuestionnaire('test_routing_not_affected_by_answers_not_on_path.json').then(openBrowser => browser = openBrowser);
  });

  it('Given the user enters an answer on the first path, when they return to the second path, they should be routed to the valid path interstitial', function() {
      $(InitialChoicePage.first()).click();
      $(InitialChoicePage.submit()).click();

      expect(browser.getUrl()).to.contain(InvalidPathPage.pageName);
      $(InvalidPathPage.answer()).setValue(123);
      $(InvalidPathPage.submit()).click();

      // We now have an answer in the store on the 'invalid' path

      expect(browser.getUrl()).to.contain(InvalidPathInterstitialPage.pageName);
      $(InvalidPathInterstitialPage.previous()).click();
      $(InvalidPathPage.previous()).click();

      // Take the second route

      $(InitialChoicePage.second()).click();
      $(InitialChoicePage.submit()).click();

      $(ValidPathPage.answer()).setValue(321);
      $(ValidPathPage.submit()).click();

      // We should be routed to the valid interstitial page since the invalid path answer should not be considered whilst routing.
      expect(browser.getUrl()).to.contain(ValidFinalInterstitialPage.pageName);
  });
});

