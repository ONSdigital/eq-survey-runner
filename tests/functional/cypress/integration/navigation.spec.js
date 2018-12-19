import {openQuestionnaire, navigationLink, isSectionComplete} from '../helpers/helpers.js'
const CreditCardPage = require('../../generated_pages/navigation/credit-card.page.js');
const ExpiryDate = require('../../generated_pages/navigation/expiry-date.page.js');
const ExtraCoverBlockPage = require('../../generated_pages/navigation/extra-cover-block.page.js');
const ExtraCoverItemsPage = require('../../generated_pages/navigation/extra-cover-items.page.js');
const ExtraCoverItemsRadioPage = require('../../generated_pages/navigation/extra-cover-items-radio.page.js');
const HouseTypePage = require('../../generated_pages/navigation/house-type.page.js');
const HouseholdCompositionPage = require('../../generated_pages/navigation/household-composition.page.js');
const InsuranceAddressPage = require('../../generated_pages/navigation/insurance-address.page.js');
const InsuranceTypePage = require('../../generated_pages/navigation/insurance-type.page.js');
const RepeatingBlock1Page = require('../../generated_pages/navigation/repeating-block-1.page.js');
const RepeatingBlock2Page = require('../../generated_pages/navigation/repeating-block-2.page.js');
const SecurityCodePage = require('../../generated_pages/navigation/security-code.page.js');
const SecurityCodeInterstitialPage = require('../../generated_pages/navigation/security-code-interstitial.page.js');
const SkipInterstitialPage = require('../../generated_pages/navigation/skip-interstitial.page.js');
const SkipPaymentPage = require('../../generated_pages/navigation/skip-payment.page.js');
const SummaryPage = require('../../generated_pages/navigation/summary.page.js');
const FinalInterstitial = require('../../generated_pages/navigation/final-interstitial.page.js');
const QuestionPage = require('../../base_pages/generic.page.js');

describe('Navigation Routing', () => {
  beforeEach(() => {
    openQuestionnaire('test_navigation_routing.json')
  })

  it('Given I have a section that can not be reached from the start of the survey, When I click on the navigation link,' +
    'Then the first block of that section should be displayed', function() {
    cy
      .navigationLink('Group 2').click()
      .get(QuestionPage.displayedName()).stripText().should('contain', 'Did you want Group 2');
  });

})
describe('Navigation', function() {

  beforeEach(() => {
    openQuestionnaire('test_navigation.json')
  })

  it('Given a page with navigation, a user should be able to see it', function() {
    cy
      .get('#section-nav').should('be.visible');
  });

  it('Given I complete all questions, all links are visible, navigateable and appropriately completed', function() {
    cy
      .then(completeAllQuestions)
      .then(() => {
        cy
          .url().should('contain', SummaryPage.pageName)
          .navigationLink('Property Details').click()
          .url().should('contain', InsuranceTypePage.pageName)
          .navigationLink('House Details').click()
          .url().should('contain', HouseTypePage.pageName)
          .navigationLink('Household Composition').click()
          .url().should('contain', HouseholdCompositionPage.pageName)
          .navigationLink('Test User').click()
          .url().should('contain', RepeatingBlock1Page.pageName)
          .navigationLink('Extra Cover').click()
          .url().should('contain', ExtraCoverBlockPage.pageName)
          .navigationLink('Extra Cover Items').click()
          .url().should('contain', ExtraCoverItemsPage.pageName)
          .navigationLink('Payment Details').click()
          .url().should('contain', SkipPaymentPage.pageName)
          .navigationLink('Summary').click()
          .url().should('contain', SummaryPage.pageName);
      });
  });

  it('Given I complete all questions then incomplete one, then summary should disappear', function() {
    cy
      .then(completeAllQuestions)
      .then(() => {
        cy
          .url().should('contain', SummaryPage.pageName)
          .navigationLink('Extra Cover').click()
          .get(ExtraCoverBlockPage.extraCover()).type('2')
          .get(ExtraCoverBlockPage.submit()).click()
          .navigationLink('Summary').should('not.be.visible');
      });
  });

  it('Given I add members to a repeating navigation group, additional member links should appear and work', function() {
    cy
      .navigationLink('Household Composition').click()
      .get(HouseholdCompositionPage.firstName()).type('Test')
      .get(HouseholdCompositionPage.lastName()).type('User')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Another')
      .get(HouseholdCompositionPage.lastName('_1')).type('User')
      .navigationLink('Test User').should('not.be.visible')
      .navigationLink('Another User').should('not.be.visible')
      .get(HouseholdCompositionPage.submit()).click()
      .navigationLink('Test User').should('be.visible')
      .navigationLink('Another User').should('be.visible')
      .navigationLink('Another User').click()
      .url().should('contain', RepeatingBlock1Page.pageName);
  });

  it('Given I add multiple members to repeating navigation group, completed status should be independent', function() {
    cy
      .navigationLink('Household Composition').click()
      .get(HouseholdCompositionPage.firstName()).type('Test')
      .get(HouseholdCompositionPage.lastName()).type('User')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Another')
      .get(HouseholdCompositionPage.lastName('_1')).type('User')
      .get(HouseholdCompositionPage.submit()).click()
      .navigationLink('Test User').should('be.visible')
      .navigationLink('Another User').should('be.visible')
      .get(RepeatingBlock1Page.yes()).click()
      .get(RepeatingBlock1Page.submit()).click()
      .get(RepeatingBlock2Page.employed()).click()
      .isSectionComplete('Test User').should('be.false')
      .isSectionComplete('Another User').should('be.false')
      .get(RepeatingBlock2Page.submit()).click()
      .isSectionComplete('Test User').should('be.true')
      .isSectionComplete('Another User').should('be.false')
  });

  it('Given I add then remove members of a repeating navigation group, additional member links should disappear', function() {
    cy
      .navigationLink('Household Composition').click()
      .get(HouseholdCompositionPage.firstName()).type('Test')
      .get(HouseholdCompositionPage.lastName()).type('User')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Another')
      .get(HouseholdCompositionPage.lastName('_1')).type('User')
      .get(HouseholdCompositionPage.submit()).click()
      .navigationLink('Test User').should('be.visible')
      .navigationLink('Another User').should('be.visible')
      .navigationLink('Household Composition').click()
      .get(HouseholdCompositionPage.removePerson(1)).click()
      // Wait until page refresh
      .get(HouseholdCompositionPage.removePerson(1), {timeout: 2000}).should('not.be.visible')
      .get(HouseholdCompositionPage.submit()).click()
      .navigationLink('Test User').should('be.visible')
      .navigationLink('Another User').should('not.be.visible');
  });

  it('Given I set a repeating group back to zero, added single repeating group link should disappear', function() {
    cy
      .navigationLink('Extra Cover').click()
      .get(ExtraCoverBlockPage.extraCover()).type('1')
      .navigationLink('Extra Cover Items').should('not.be.visible')
      .get(ExtraCoverBlockPage.submit()).click()
      .navigationLink('Extra Cover Items').should('be.visible')
      .navigationLink('Extra Cover').click()
      .get(ExtraCoverBlockPage.extraCover()).clear()
      .get(ExtraCoverBlockPage.extraCover()).type('0')
      .get(ExtraCoverBlockPage.submit()).click()
      .navigationLink('Extra Cover Items').should('not.be.visible');
  });

  function completeAllQuestions() {
    return cy
      .get(InsuranceTypePage.both()).click()
      .get(InsuranceTypePage.submit()).click()
      .get(InsuranceAddressPage.answer()).type('Address')
      .isSectionComplete('Property Details').should('be.false')
      .get(InsuranceAddressPage.submit()).click()
      .isSectionComplete('Property Details').should('be.true')
      .get(HouseTypePage.detached()).click()
      .isSectionComplete('House Details').should('be.false')
      .get(HouseTypePage.submit()).click()
      .isSectionComplete('House Details').should('be.true')
      .get(HouseholdCompositionPage.firstName()).type('Test')
      .get(HouseholdCompositionPage.lastName()).type('User')
      .isSectionComplete('Household Composition').should('be.false')
      .get(HouseholdCompositionPage.submit()).click()
      .isSectionComplete('Household Composition').should('be.true')
      .get(RepeatingBlock1Page.yes()).click()
      .get(RepeatingBlock1Page.submit()).click()
      .get(RepeatingBlock2Page.employed()).click()
      .isSectionComplete('Test User').should('be.false')
      .get(RepeatingBlock2Page.submit()).click()
      .isSectionComplete('Test User').should('be.true')
      .get(ExtraCoverBlockPage.extraCover()).type('1')
      .isSectionComplete('Extra Cover').should('be.false')
      .get(ExtraCoverBlockPage.submit()).click()
      .isSectionComplete('Extra Cover').should('be.true')
      .get(ExtraCoverItemsPage.answer()).type('1')
      .get(ExtraCoverItemsPage.submit()).click()
      .get(ExtraCoverItemsRadioPage.yes()).click()
      .isSectionComplete('Extra Cover Items').should('be.false')
      .get(ExtraCoverItemsRadioPage.submit()).click()
      .isSectionComplete('Extra Cover Items').should('be.true')
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
      .isSectionComplete('Payment Details').should('be.true')
  }

});
