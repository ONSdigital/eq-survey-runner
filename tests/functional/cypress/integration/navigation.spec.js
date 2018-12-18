import {openQuestionnaire} from ../helpers/helpers.js
const CreditCardPage = require('../generated_pages/navigation/credit-card.page.js');
const ExpiryDate = require('../generated_pages/navigation/expiry-date.page.js');
const ExtraCoverBlockPage = require('../generated_pages/navigation/extra-cover-block.page.js');
const ExtraCoverItemsPage = require('../generated_pages/navigation/extra-cover-items.page.js');
const ExtraCoverItemsRadioPage = require('../generated_pages/navigation/extra-cover-items-radio.page.js');
const HouseTypePage = require('../generated_pages/navigation/house-type.page.js');
const HouseholdCompositionPage = require('../generated_pages/navigation/household-composition.page.js');
const InsuranceAddressPage = require('../generated_pages/navigation/insurance-address.page.js');
const InsuranceTypePage = require('../generated_pages/navigation/insurance-type.page.js');
const RepeatingBlock1Page = require('../generated_pages/navigation/repeating-block-1.page.js');
const RepeatingBlock2Page = require('../generated_pages/navigation/repeating-block-2.page.js');
const SecurityCodePage = require('../generated_pages/navigation/security-code.page.js');
const SecurityCodeInterstitialPage = require('../generated_pages/navigation/security-code-interstitial.page.js');
const SkipInterstitialPage = require('../generated_pages/navigation/skip-interstitial.page.js');
const SkipPaymentPage = require('../generated_pages/navigation/skip-payment.page.js');
const SummaryPage = require('../generated_pages/navigation/summary.page.js');
const FinalInterstitial = require('../generated_pages/navigation/final-interstitial.page.js');
const QuestionPage = require('../base_pages/generic.page.js');



describe('Navigation', function() {

  it('Given a page with navigation, a user should be able to see it', function() {
    openQuestionnaire('test_navigation.json')
              .isVisible('#section-nav').should.eventually.be.true;
      });
  });

  it('Given I complete all questions, all links are visible, navigateable and appropriately completed', function() {
    return helpers.openQuestionnaire('test_navigation.json')
    .then(completeAllQuestions)
    .then(() => {
              .url().should('contain', SummaryPage.pageName)
        .get(helpers.navigationLink('Property Details')).click()
        .url().should('contain', InsuranceTypePage.pageName)
        .get(helpers.navigationLink('House Details')).click()
        .url().should('contain', HouseTypePage.pageName)
        .get(helpers.navigationLink('Household Composition')).click()
        .url().should('contain', HouseholdCompositionPage.pageName)
        .get(helpers.navigationLink('Test User')).click()
        .url().should('contain', RepeatingBlock1Page.pageName)
        .get(helpers.navigationLink('Extra Cover')).click()
        .url().should('contain', ExtraCoverBlockPage.pageName)
        .get(helpers.navigationLink('Extra Cover Items')).click()
        .url().should('contain', ExtraCoverItemsPage.pageName)
        .get(helpers.navigationLink('Payment Details')).click()
        .url().should('contain', SkipPaymentPage.pageName)
        .get(helpers.navigationLink('Summary')).click()
        .url().should('contain', SummaryPage.pageName);
      });
  });

  it('Given I complete all questions then incomplete one, then summary should disappear', function() {
    return helpers.openQuestionnaire('test_navigation.json')
    .then(completeAllQuestions)
    .then(() => {
              .url().should('contain', SummaryPage.pageName)
        .get(helpers.navigationLink('Extra Cover')).click()
        .get(ExtraCoverBlockPage.extraCover()).type('2')
        .get(ExtraCoverBlockPage.submit()).click()
        .isVisible(helpers.navigationLink('Summary')).should.eventually.be.false;
      });
  });

  it('Given I add members to a repeating navigation group, additional member links should appear and work', function() {
    openQuestionnaire('test_navigation.json')
              .get(helpers.navigationLink('Household Composition')).click()
        .get(HouseholdCompositionPage.firstName()).type('Test')
        .get(HouseholdCompositionPage.lastName()).type('User')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_1')).type('Another')
        .get(HouseholdCompositionPage.lastName('_1')).type('User')
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.false
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.false
        .get(HouseholdCompositionPage.submit()).click()
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.true
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.true
        .get(helpers.navigationLink('Another User')).click()
        .url().should('contain', RepeatingBlock1Page.pageName);
      });
  });

  it('Given I add multiple members to repeating navigation group, completed status should be independent', function() {
    openQuestionnaire('test_navigation.json')
              .get(helpers.navigationLink('Household Composition')).click()
        .get(HouseholdCompositionPage.firstName()).type('Test')
        .get(HouseholdCompositionPage.lastName()).type('User')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_1')).type('Another')
        .get(HouseholdCompositionPage.lastName('_1')).type('User')
        .get(HouseholdCompositionPage.submit()).click()
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.true
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.true
        .get(RepeatingBlock1Page.yes()).click()
        .get(RepeatingBlock1Page.submit()).click()
        .get(RepeatingBlock2Page.employed()).click()
        .then(helpers.isSectionComplete('Test User')).should.eventually.be.false
        .then(helpers.isSectionComplete('Another User')).should.eventually.be.false
        .get(RepeatingBlock2Page.submit()).click()
        .then(helpers.isSectionComplete('Test User')).should.eventually.be.true
        .then(helpers.isSectionComplete('Another User')).should.eventually.be.false;
      });
  });

  it('Given I add then remove members of a repeating navigation group, additional member links should disappear', function() {
    openQuestionnaire('test_navigation.json')
              .get(helpers.navigationLink('Household Composition')).click()
        .get(HouseholdCompositionPage.firstName()).type('Test')
        .get(HouseholdCompositionPage.lastName()).type('User')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_1')).type('Another')
        .get(HouseholdCompositionPage.lastName('_1')).type('User')
        .get(HouseholdCompositionPage.submit()).click()
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.true
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.true
        .get(helpers.navigationLink('Household Composition')).click()
        .get(HouseholdCompositionPage.removePerson(1)).click()
        // Wait until page refresh
        .get(HouseholdCompositionPage.removePerson(1), {timeout: 2000}).should('exist')
        .get(HouseholdCompositionPage.submit()).click()
        .isVisible(helpers.navigationLink('Test User')).should.eventually.be.true
        .isVisible(helpers.navigationLink('Another User')).should.eventually.be.false;
      });
  });

  it('Given I set a repeating group back to zero, added single repeating group link should disappear', function() {
    openQuestionnaire('test_navigation.json')
              .get(helpers.navigationLink('Extra Cover')).click()
        .get(ExtraCoverBlockPage.extraCover()).type('1')
        .isVisible(helpers.navigationLink('Extra Cover Items')).should.eventually.be.false
        .get(ExtraCoverBlockPage.submit()).click()
        .isVisible(helpers.navigationLink('Extra Cover Items')).should.eventually.be.true
        .get(helpers.navigationLink('Extra Cover')).click()
        .get(ExtraCoverBlockPage.extraCover()).type('0')
        .get(ExtraCoverBlockPage.submit()).click()
        .isVisible(helpers.navigationLink('Extra Cover Items')).should.eventually.be.false;
      });
  });

  it('Given I have a section that can not be reached from the start of the survey, When I click on the navigation link,' +
    ' Then the first block of that section should be displayed', function() {
    openQuestionnaire('test_navigation_routing.json')
              .get(helpers.navigationLink('Group 2')).click()
        .get(QuestionPage.displayedName()).stripText().should('contain', 'Did you want Group 2');
      });
  });

  function completeAllQuestions() {
      .get(InsuranceTypePage.both()).click()
    .get(InsuranceTypePage.submit()).click()
    .get(InsuranceAddressPage.answer()).type('Address')
    .then(helpers.isSectionComplete('Property Details')).should.eventually.be.false
    .get(InsuranceAddressPage.submit()).click()
    .then(helpers.isSectionComplete('Property Details')).should.eventually.be.true
    .get(HouseTypePage.detached()).click()
    .then(helpers.isSectionComplete('House Details')).should.eventually.be.false
    .get(HouseTypePage.submit()).click()
    .then(helpers.isSectionComplete('House Details')).should.eventually.be.true
    .get(HouseholdCompositionPage.firstName()).type('Test')
    .get(HouseholdCompositionPage.lastName()).type('User')
    .then(helpers.isSectionComplete('Household Composition')).should.eventually.be.false
    .get(HouseholdCompositionPage.submit()).click()
    .then(helpers.isSectionComplete('Household Composition')).should.eventually.be.true
    .get(RepeatingBlock1Page.yes()).click()
    .get(RepeatingBlock1Page.submit()).click()
    .get(RepeatingBlock2Page.employed()).click()
    .then(helpers.isSectionComplete('Test User')).should.eventually.be.false
    .get(RepeatingBlock2Page.submit()).click()
    .then(helpers.isSectionComplete('Test User')).should.eventually.be.true
    .get(ExtraCoverBlockPage.extraCover()).type('1')
    .then(helpers.isSectionComplete('Extra Cover')).should.eventually.be.false
    .get(ExtraCoverBlockPage.submit()).click()
    .then(helpers.isSectionComplete('Extra Cover')).should.eventually.be.true
    .get(ExtraCoverItemsPage.answer()).type('1')
    .get(ExtraCoverItemsPage.submit()).click()
    .get(ExtraCoverItemsRadioPage.yes()).click()
    .then(helpers.isSectionComplete('Extra Cover Items')).should.eventually.be.false
    .get(ExtraCoverItemsRadioPage.submit()).click()
    .then(helpers.isSectionComplete('Extra Cover Items')).should.eventually.be.true
    .get(SkipPaymentPage.no()).click()
    .get(SkipPaymentPage.submit()).click()
    .get(CreditCardPage.answer()).type('1234567890')
    .get(CreditCardPage.submit()).click()
    .get(ExpiryDate.answer()).type('1234')
    .get(ExpiryDate.submit()).click()
    .get(SecurityCodePage.answer()).type('123')
    .get(SecurityCodePage.submit()).click()
    .get(SkipInterstitialPage.no()).click()
    .get(SkipInterstitialPage.submit()).click()
    .get(SecurityCodeInterstitialPage.submit()).click()
    .get(FinalInterstitial.submit()).click()
    .then(helpers.isSectionComplete('Payment Details')).should.eventually.be.true;
  }

});
