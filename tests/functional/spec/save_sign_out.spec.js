const helpers = require('../helpers');
const utilities = require('../utilities');
const SetMinMax = require('../generated_pages/numbers/set-min-max-block.page.js');
const TestMinMax = require('../generated_pages/numbers/test-min-max-block.page.js');
const SummaryPage = require('../generated_pages/numbers/summary.page');

const IntroductionPage = require('../generated_pages/introduction/introduction.page');
const IntroInterstitialPage = require('../generated_pages/introduction/general-business-information-completed.page');
const IntroConfirmationPage = require('../generated_pages/introduction/confirmation.page');
const IntroThankYouPagePage = require('../base_pages/thank-you.page');

const NIRadioPage = require('../generated_pages/theme_northernireland/radio.page');
const NISummaryPage = require('../generated_pages/theme_northernireland/summary.page');
const NIThankYouPage = require('../base_pages/thank-you.page');
const NIViewSubmissionPage = require('../base_pages/thank-you.page');

const SocialRadioPage = require('../generated_pages/theme_social/radio.page');
const SocialSummaryPage = require('../generated_pages/theme_social/summary.page');
const SocialThankYouPage = require('../base_pages/thank-you.page');
const SocialViewSubmissionPage = require('../base_pages/thank-you.page');

const FeedbackForm = require('../base_pages/feedback-form');

describe('SaveSignOut', function() {

  const responseId = utilities.getRandomString(16);

  it('Given I am completing a survey, when I select save and complete later, then I am redirected to sign out page and my session is cleared', function() {
    return helpers.openQuestionnaire('test_numbers.json', { userId: 'test_user', responseId: responseId } ).then(() => {
        return browser
          .setValue(SetMinMax.setMinimum(), '10')
          .setValue(SetMinMax.setMaximum(), '1020')
          .click(SetMinMax.submit())
          .click(TestMinMax.saveSignOut())
          .getUrl().should.eventually.contain('localhost')
          .back()
          .getSource().should.eventually.contain('Your session has expired');
      });
  });

  it('Given I have started a questionnaire, when I return to the questionnaire, then I am returned to the page I was on and can then complete the survey', function() {
    return helpers.openQuestionnaire('test_numbers.json', { userId: 'test_user', responseId: responseId } ).then(() => {
        return browser
          .getUrl().should.eventually.contain(TestMinMax.pageName)
          .setValue(TestMinMax.testRange(), '10')
          .setValue(TestMinMax.testMin(), '123')
          .setValue(TestMinMax.testMax(), '1000')
          .setValue(TestMinMax.testPercent(), '100')
          .click(TestMinMax.submit())
          .getUrl().should.eventually.contain(SummaryPage.pageName)
          .click(SummaryPage.submit())
          .getUrl().should.eventually.contain('thank-you');
      });
  });

  it('Given a logout url is set, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    return helpers.openQuestionnaire('test_introduction.json', { includeLogoutUrl: true }).then(() => {
        return browser
          .getUrl().should.eventually.contain(IntroductionPage.pageName)
          .getText(IntroductionPage.signOut()).should.eventually.contain('Sign out')
          .click(IntroductionPage.getStarted())

          .getUrl().should.eventually.contain(IntroInterstitialPage.pageName)
          .getText(IntroInterstitialPage.saveSignOut()).should.eventually.contain('Save and sign out')
          .click(IntroInterstitialPage.submit())

          .getUrl().should.eventually.contain(IntroConfirmationPage.pageName)
          .getText(IntroConfirmationPage.saveSignOut()).should.eventually.contain('Save and sign out')
          .click(IntroConfirmationPage.submit())

          .getUrl().should.eventually.contain(IntroThankYouPagePage.pageName)
          .getText(IntroThankYouPagePage.signOut()).should.eventually.contain('Sign out');
      });
  });

  it('Given a logout url is not set, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    return helpers.openQuestionnaire('test_introduction.json', { includeLogoutUrl: false }).then(() => {
        return browser
          .getUrl().should.eventually.contain(IntroductionPage.pageName)
          .isExisting(IntroductionPage.signOut()).should.eventually.be.false
          .click(IntroductionPage.getStarted())

          .getUrl().should.eventually.contain(IntroInterstitialPage.pageName)
          .getText(IntroInterstitialPage.saveSignOut()).should.eventually.contain('Save and complete later')
          .click(IntroInterstitialPage.submit())

          .getUrl().should.eventually.contain(IntroConfirmationPage.pageName)
          .getText(IntroConfirmationPage.saveSignOut()).should.eventually.contain('Save and complete later')
          .click(IntroConfirmationPage.submit())

          .getUrl().should.eventually.contain(IntroThankYouPagePage.pageName)
          .isExisting(IntroductionPage.signOut()).should.eventually.be.false;
      });
  });

  it('Given I am on a northern ireland themed survey, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    return helpers.openQuestionnaire('test_theme_northernireland.json', { includeLogoutUrl: true }).then(() => {
        return browser
          .getUrl().should.eventually.contain(NIRadioPage.pageName)
          .getText(NIRadioPage.saveSignOut()).should.eventually.contain('Save and sign out')
          .click(NIRadioPage.submit())
          .getUrl().should.eventually.contain(NISummaryPage.pageName)
          .getText(NISummaryPage.saveSignOut()).should.eventually.contain('Save and sign out')
          .click(NISummaryPage.submit())
          .getUrl().should.eventually.contain(NIThankYouPage.pageName)
          .getText(NIThankYouPage.signOut()).should.eventually.contain('Sign out')
          .click(NIThankYouPage.viewSubmitted())
          .getUrl().should.eventually.contain('view-submission')
          .getText(NIViewSubmissionPage.signOut()).should.eventually.contain('Sign out');
      });
  });

  it('Given I am on a social themed survey, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    return helpers.openQuestionnaire('test_theme_social.json', { includeLogoutUrl: false } ).then(() => {
        return browser
          .getUrl().should.eventually.contain(SocialRadioPage.pageName)
          .getText(SocialRadioPage.saveSignOut()).should.eventually.contain('Save and complete later')
          .click(SocialRadioPage.submit())
          .getUrl().should.eventually.contain(SocialSummaryPage.pageName)
          .getText(SocialSummaryPage.saveSignOut()).should.eventually.contain('Save and complete later')
          .click(SocialSummaryPage.submit())
          .getUrl().should.eventually.contain(SocialThankYouPage.pageName)
          .isExisting(SocialThankYouPage.signOut()).should.eventually.be.false
          .click(SocialThankYouPage.viewSubmitted())
          .getUrl().should.eventually.contain('view-submission')
          .isExisting(SocialViewSubmissionPage.signOut()).should.eventually.be.false;
      });
  });

  it('Given a logout url is set, when I load the feedback page, then I see the sign out button', function() {
    return helpers.openQuestionnaire('test_numbers.json', { includeLogoutUrl: true }).then(() => {
        return browser
          .url(FeedbackForm.url())
          .getUrl().should.eventually.contain('feedback')
          .isExisting(FeedbackForm.signOut()).should.eventually.be.true
          .getText(FeedbackForm.signOut()).should.eventually.contain('Sign out');
      });
  });

  it('Given a logout url is not set, when I load the feedback page, then there should be no sign out button', function() {
    return helpers.openQuestionnaire('test_numbers.json', { includeLogoutUrl: false }).then(() => {
        return browser
          .url(FeedbackForm.url())
          .getUrl().should.eventually.contain('feedback')
          .isExisting(FeedbackForm.signOut()).should.eventually.be.false;
      });
  });

  it('Given a logout url is set and I load the feedback page, when I sign out, then I should be on the account service logged out page', function() {
    return helpers.openQuestionnaire('test_numbers.json', { includeLogoutUrl: true }).then(() => {
        return browser
          .url(FeedbackForm.url())
          .getUrl().should.eventually.contain('feedback')
          .isExisting(FeedbackForm.signOut()).should.eventually.be.true
          .click(FeedbackForm.signOut())
          .getUrl().should.eventually.contain('http://localhost:8000');
      });
  });

});
