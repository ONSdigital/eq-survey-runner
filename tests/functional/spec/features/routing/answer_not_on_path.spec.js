const helpers = require('../../../helpers');

const InitialChoicePage = require('../../../pages/features/routing/answer_value_off_path/initial-choice.page.js');
const InvalidPathPage = require('../../../pages/features/routing/answer_value_off_path/invalid-path.page.js');
const InvalidPathInterstitialPage = require('../../../pages/features/routing/answer_value_off_path/invalid-path-interstitial.page.js');
const ValidPathPage = require('../../../pages/features/routing/answer_value_off_path/valid-path.page.js');
const ValidFinalInterstitialPage = require('../../../pages/features/routing/answer_value_off_path/valid-final-interstitial.page.js');

describe('Answers not on path are not considered when routing', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_routing_not_affected_by_answers_not_on_path.json');
  });

  it('Given the user enters an answer on the first path, when they return to the second path, they should be routed to the valid path interstitial', function() {
    return browser
      .click(InitialChoicePage.first())
      .click(InitialChoicePage.submit())

      .getUrl().should.eventually.contain(InvalidPathPage.pageName)
      .setValue(InvalidPathPage.answer(), 123)
      .click(InvalidPathPage.submit())

      // We now have an answer in the store on the 'invalid' path

      .getUrl().should.eventually.contain(InvalidPathInterstitialPage.pageName)
      .click(InvalidPathInterstitialPage.previous())
      .click(InvalidPathPage.previous())

      // Take the second route

      .click(InitialChoicePage.second())
      .click(InitialChoicePage.submit())

      .setValue(ValidPathPage.answer(), 321)
      .click(ValidPathPage.submit())

      // We should be routed to the valid interstitial page since the invalid path answer should not be considered whilst routing.
      .getUrl().should.eventually.contain(ValidFinalInterstitialPage.pageName);
  });
});

