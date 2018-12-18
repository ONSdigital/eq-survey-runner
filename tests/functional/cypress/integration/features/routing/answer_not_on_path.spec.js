import {openQuestionnaire} from ../../../helpers/helpers.js

const InitialChoicePage =           require('../../../../generated_pages/routing_not_affected_by_answers_not_on_path/initial-choice.page.js');
const InvalidPathPage =             require('../../../../generated_pages/routing_not_affected_by_answers_not_on_path/invalid-path.page.js');
const InvalidPathInterstitialPage = require('../../../../generated_pages/routing_not_affected_by_answers_not_on_path/invalid-path-interstitial.page.js');
const ValidPathPage =               require('../../../generated_pages/routing_not_affected_by_answers_not_on_path/valid-path.page.js');
const ValidFinalInterstitialPage =  require('../../../generated_pages/routing_not_affected_by_answers_not_on_path/valid-final-interstitial.page.js');

describe('Answers not on path are not considered when routing', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_routing_not_affected_by_answers_not_on_path.json');
  });

  it('Given the user enters an answer on the first path, when they return to the second path, they should be routed to the valid path interstitial', function() {
          .get(InitialChoicePage.first()).click()
      .get(InitialChoicePage.submit()).click()

      .url().should('contain', InvalidPathPage.pageName)
      .get(InvalidPathPage.answer()).type(123)
      .get(InvalidPathPage.submit()).click()

      // We now have an answer in the store on the 'invalid' path

      .url().should('contain', InvalidPathInterstitialPage.pageName)
      .get(InvalidPathInterstitialPage.previous()).click()
      .get(InvalidPathPage.previous()).click()

      // Take the second route

      .get(InitialChoicePage.second()).click()
      .get(InitialChoicePage.submit()).click()

      .get(ValidPathPage.answer()).type(321)
      .get(ValidPathPage.submit()).click()

      // We should be routed to the valid interstitial page since the invalid path answer should not be considered whilst routing.
      .url().should('contain', ValidFinalInterstitialPage.pageName);
  });
});

