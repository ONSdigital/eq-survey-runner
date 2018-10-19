const helpers = require('../helpers');
const CreditCardPage = require('../pages/surveys/navigation/credit-card.page.js');
const ExpiryDate = require('../pages/surveys/navigation/expiry-date.page.js');
const ExtraCoverBlockPage = require('../pages/surveys/navigation/extra-cover-block.page.js');
const ExtraCoverItemsPage = require('../pages/surveys/navigation/extra-cover-items.page.js');
const ExtraCoverItemsRadioPage = require('../pages/surveys/navigation/extra-cover-items-radio.page.js');
const HouseTypePage = require('../pages/surveys/navigation/house-type.page.js');
const HouseholdCompositionPage = require('../pages/surveys/navigation/household-composition.page.js');
const InsuranceAddressPage = require('../pages/surveys/navigation/insurance-address.page.js');
const InsuranceTypePage = require('../pages/surveys/navigation/insurance-type.page.js');
const RepeatingBlock1Page = require('../pages/surveys/navigation/repeating-block-1.page.js');
const RepeatingBlock2Page = require('../pages/surveys/navigation/repeating-block-2.page.js');
const SecurityCodePage = require('../pages/surveys/navigation/security-code.page.js');
const SecurityCodeInterstitialPage = require('../pages/surveys/navigation/security-code-interstitial.page.js');
const SkipInterstitialPage = require('../pages/surveys/navigation/skip-interstitial.page.js');
const SkipPaymentPage = require('../pages/surveys/navigation/skip-payment.page.js');
const SummaryPage = require('../pages/surveys/navigation/summary.page.js');
const FinalInterstitial = require('../pages/surveys/navigation/final-interstitial.page.js');
const GenericPage = require('../pages/surveys/generic.page.js');

const CoffeePage = require('../pages/surveys/navigation/completeness/coffee.page.js');
const ResponseYesPage = require('../pages/surveys/navigation/completeness/response-yes.page.js');
const ResponseNoPage = require('../pages/surveys/navigation/completeness/response-no.page.js');


describe('Navigation', function() {

  it('Given a page with navigation, a user should be able to see it', function() {
    return helpers.openQuestionnaire('test_navigation.json').then(() => {
      return browser
        .isVisible('#section-nav').should.eventually.be.true;
      });
  });

  it('Given I complete all questions, all links are visible, navigateable and appropriately completed', function() {
    return helpers.openQuestionnaire('test_navigation.json')
    .then(completeAllQuestions)
    .then(() => {
      return browser
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .click(helpers.navigationLink('Property Details'))
        .getUrl().should.eventually.contain(InsuranceTypePage.pageName)
        .click(helpers.navigationLink('House Details'))
        .getUrl().should.eventually.contain(HouseTypePage.pageName)
        .click(helpers.navigationLink('Household Composition'))
        .getUrl().should.eventually.contain(HouseholdCompositionPage.pageName)
        .click(helpers.navigationLink('Test User'))
        .getUrl().should.eventually.contain(RepeatingBlock1Page.pageName)
        .click(helpers.navigationLink('Extra Cover'))
        .getUrl().should.eventually.contain(ExtraCoverBlockPage.pageName)
        .click(helpers.navigationLink('Extra Cover Items'))
        .getUrl().should.eventually.contain(ExtraCoverItemsPage.pageName)
        .click(helpers.navigationLink('Payment Details'))
        .getUrl().should.eventually.contain(SkipPaymentPage.pageName)
        .click(helpers.navigationLink('Summary'))
        .getUrl().should.eventually.contain(SummaryPage.pageName);
      });
  });

  it('Given I complete all questions then incomplete one, then summary should disappear', function() {
    return helpers.openQuestionnaire('test_navigation.json')
    .then(completeAllQuestions)
    .then(() => {
      return browser
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .click(helpers.navigationLink('Extra Cover'))
        .setValue(ExtraCoverBlockPage.answer(), '2')
        .click(ExtraCoverBlockPage.submit())
        .isVisible(helpers.navigationLink('Summary')).should.eventually.be.false;
      });
  });

  it('Given I add members to a repeating navigation group, additional member links should appear and work', function() {
    return helpers.openQuestionnaire('test_navigation.json').then(() => {
      return browser
        .click(helpers.navigationLink('Household Composition'))
        .setValue(HouseholdCompositionPage.firstName(), 'Test')
        .setValue(HouseholdCompositionPage.lastName(), 'User')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.firstName('_1'), 'Another')
        .setValue(HouseholdCompositionPage.lastName('_1'), 'User')
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.false
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.false
        .click(HouseholdCompositionPage.submit())
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.true
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.true
        .click(helpers.navigationLink('Another User'))
        .getUrl().should.eventually.contain(RepeatingBlock1Page.pageName);
      });
  });

  it('Given I add multiple members to repeating navigation group, completed status should be independent', function() {
    return helpers.openQuestionnaire('test_navigation.json').then(() => {
      return browser
        .click(helpers.navigationLink('Household Composition'))
        .setValue(HouseholdCompositionPage.firstName(), 'Test')
        .setValue(HouseholdCompositionPage.lastName(), 'User')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.firstName('_1'), 'Another')
        .setValue(HouseholdCompositionPage.lastName('_1'), 'User')
        .click(HouseholdCompositionPage.submit())
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.true
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.true
        .click(RepeatingBlock1Page.yes())
        .click(RepeatingBlock1Page.submit())
        .click(RepeatingBlock2Page.employed())
        .then(helpers.isSectionComplete('Test User')).should.eventually.be.false
        .then(helpers.isSectionComplete('Another User')).should.eventually.be.false
        .click(RepeatingBlock2Page.submit())
        .then(helpers.isSectionComplete('Test User')).should.eventually.be.true
        .then(helpers.isSectionComplete('Another User')).should.eventually.be.false;
      });
  });

  it('Given I add then remove members of a repeating navigation group, additional member links should disappear', function() {
    return helpers.openQuestionnaire('test_navigation.json').then(() => {
      return browser
        .click(helpers.navigationLink('Household Composition'))
        .setValue(HouseholdCompositionPage.firstName(), 'Test')
        .setValue(HouseholdCompositionPage.lastName(), 'User')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.firstName('_1'), 'Another')
        .setValue(HouseholdCompositionPage.lastName('_1'), 'User')
        .click(HouseholdCompositionPage.submit())
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.true
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.true
        .click(helpers.navigationLink('Household Composition'))
        .click(HouseholdCompositionPage.removePerson())
        // Wait until page refresh
        .waitForExist(HouseholdCompositionPage.removePerson(), 2000, true)
        .click(HouseholdCompositionPage.submit())
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.true
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.false;
      });
  });

  it('Given I set a repeating group back to zero, added single repeating group link should disappear', function() {
    return helpers.openQuestionnaire('test_navigation.json').then(() => {
      return browser
        .click(helpers.navigationLink('Extra Cover'))
        .setValue(ExtraCoverBlockPage.answer(), '1')
        .isVisible(helpers.navigationLink('Extra Cover Items')).should.eventually.be.false
        .click(ExtraCoverBlockPage.submit())
        .isVisible(helpers.navigationLink('Extra Cover Items')).should.eventually.be.true
        .click(helpers.navigationLink('Extra Cover'))
        .setValue(ExtraCoverBlockPage.answer(), '0')
        .click(ExtraCoverBlockPage.submit())
        .isVisible(helpers.navigationLink('Extra Cover Items')).should.eventually.be.false;
      });
  });

  it('Given I have a section that can not be reached from the start of the survey, When I click on the navigation link,' +
    ' Then the first block of that section should be displayed', function() {
    return helpers.openQuestionnaire('test_navigation_routing.json').then(() => {
      return browser
        .click(helpers.navigationLink('Group 2'))
        .getText(GenericPage.displayedName()).should.eventually.contain('Did you want Group 2');
      });
  });

  function completeAllQuestions() {
  return browser
    .click(InsuranceTypePage.both())
    .click(InsuranceTypePage.submit())
    .setValue(InsuranceAddressPage.answer(), 'Address')
    .then(helpers.isSectionComplete('Property Details')).should.eventually.be.false
    .click(InsuranceAddressPage.submit())
    .then(helpers.isSectionComplete('Property Details')).should.eventually.be.true
    .click(HouseTypePage.detached())
    .then(helpers.isSectionComplete('House Details')).should.eventually.be.false
    .click(HouseTypePage.submit())
    .then(helpers.isSectionComplete('House Details')).should.eventually.be.true
    .setValue(HouseholdCompositionPage.firstName(), 'Test')
    .setValue(HouseholdCompositionPage.lastName(), 'User')
    .then(helpers.isSectionComplete('Household Composition')).should.eventually.be.false
    .click(HouseholdCompositionPage.submit())
    .then(helpers.isSectionComplete('Household Composition')).should.eventually.be.true
    .click(RepeatingBlock1Page.yes())
    .click(RepeatingBlock1Page.submit())
    .click(RepeatingBlock2Page.employed())
    .then(helpers.isSectionComplete('Test User')).should.eventually.be.false
    .click(RepeatingBlock2Page.submit())
    .then(helpers.isSectionComplete('Test User')).should.eventually.be.true
    .setValue(ExtraCoverBlockPage.answer(), '1')
    .then(helpers.isSectionComplete('Extra Cover')).should.eventually.be.false
    .click(ExtraCoverBlockPage.submit())
    .then(helpers.isSectionComplete('Extra Cover')).should.eventually.be.true
    .setValue(ExtraCoverItemsPage.answer(), '1')
    .click(ExtraCoverItemsPage.submit())
    .click(ExtraCoverItemsRadioPage.yes())
    .then(helpers.isSectionComplete('Extra Cover Items')).should.eventually.be.false
    .click(ExtraCoverItemsRadioPage.submit())
    .then(helpers.isSectionComplete('Extra Cover Items')).should.eventually.be.true
    .click(SkipPaymentPage.no())
    .click(SkipPaymentPage.submit())
    .setValue(CreditCardPage.answer(), '1234567890')
    .click(CreditCardPage.submit())
    .setValue(ExpiryDate.answer(), '1234')
    .click(ExpiryDate.submit())
    .setValue(SecurityCodePage.answer(), '123')
    .click(SecurityCodePage.submit())
    .click(SkipInterstitialPage.no())
    .click(SkipInterstitialPage.submit())
    .click(SecurityCodeInterstitialPage.submit())
    .click(FinalInterstitial.submit())
    .then(helpers.isSectionComplete('Payment Details')).should.eventually.be.true;
  }

  describe('Completeness', function() {

    before("Launch Survey", function () {
      return helpers.openQuestionnaire('test_navigation_completeness.json');
    });

    it("When I complete a section then it should be marked complete", function () {
      return browser
        .click(CoffeePage.yes())
        .click(CoffeePage.submit())
        .setValue(ResponseYesPage.answer(), 2)
        .click(ResponseYesPage.submit())
        .then(helpers.isSectionComplete('Coffee')).should.eventually.be.true;
    });

    it("When I go back and change the routing path the section should be marked as incomplete", function () {
      return browser
        .click(helpers.navigationLink("Coffee"))
        .click(CoffeePage.no())
        .click(CoffeePage.submit())
        .then(helpers.isSectionComplete('Coffee')).should.eventually.be.false;
    });

    it("When I complete the new path, then the section is marked as complete", function () {
      return browser
        .setValue(ResponseNoPage.answer(), 5)
        .click(ResponseNoPage.submit())
        .then(helpers.isSectionComplete('Coffee')).should.eventually.be.true;
    });
  });

});
