const ListCollectorPage = require('../generated_pages/skip_condition_list/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/skip_condition_list/list-collector-add.page.js');
const LessThanTwoInterstitialPage = require('../generated_pages/skip_condition_list/less-than-two-interstitial.page.js');
const TwoInterstitialPage = require('../generated_pages/skip_condition_list/two-interstitial.page.js');
const MoreThanTwoInterstitialPage = require('../generated_pages/skip_condition_list/more-than-two-interstitial.page.js');

const helpers = require('../helpers');

describe('Feature: Routing on lists', function () {
  describe('Given I start skip condition list survey', function () {

    beforeEach(function () {
      return helpers.openQuestionnaire('test_skip_condition_list.json');
    });

    it('When I don\'t add a person to the list, Then the less than two people skippable page should be shown', function() {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(LessThanTwoInterstitialPage.pageName);
    });

    it('When I add one person to the list, Then the less than two people skippable page should be shown', function() {
      return browser
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Marcus')
        .setValue(ListCollectorAddPage.lastName(), 'Twin')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(LessThanTwoInterstitialPage.pageName);
    });

    it('When I add two people to the list, Then the two people skippable page should be shown', function() {
      return browser
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Marcus')
        .setValue(ListCollectorAddPage.lastName(), 'Twin')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Samuel')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(TwoInterstitialPage.pageName);
    });

    it('When I add three people to the list, Then the more than two people skippable page should be shown', function() {
      return browser
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Marcus')
        .setValue(ListCollectorAddPage.lastName(), 'Twin')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Samuel')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Olivia')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(MoreThanTwoInterstitialPage.pageName);
    });

  });
});
