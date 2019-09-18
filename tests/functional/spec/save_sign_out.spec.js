const helpers = require('../helpers');
const utilities = require('../utilities');
const SetMinMax = require('../generated_pages/numbers/set-min-max-block.page.js');
const TestMinMax = require('../generated_pages/numbers/test-min-max-block.page.js');
const SummaryPage = require('../generated_pages/numbers/summary.page');

const IntroductionPage = require('../generated_pages/introduction/introduction.page');
const IntroInterstitialPage = require('../generated_pages/introduction/general-business-information-completed.page');
const IntroConfirmationPage = require('../generated_pages/introduction/confirmation.page');
const IntroThankYouPagePage = require('../base_pages/thank-you.page');

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
          .getUrl()
          .setValue(TestMinMax.testRange(), '10')
          .setValue(TestMinMax.testMin(), '123')
          .setValue(TestMinMax.testMax(), '1000')
          .setValue(TestMinMax.testPercent(), '100')
          .click(TestMinMax.submit())
          .getUrl()
          .click(SummaryPage.submit())
          .getUrl().should.eventually.contain('thank-you');
      });
  });

  it('Given a logout url is set, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    return helpers.openQuestionnaire('test_introduction.json', { includeLogoutUrl: true }).then(() => {
        return browser
          .getUrl()
          .getText(IntroductionPage.signOut()).should.eventually.contain('Sign out')
          .click(IntroductionPage.getStarted())

          .getUrl()
          .getText(IntroInterstitialPage.saveSignOut()).should.eventually.contain('Save and sign out')
          .click(IntroInterstitialPage.submit())

          .getUrl()
          .getText(IntroConfirmationPage.saveSignOut()).should.eventually.contain('Save and sign out')
          .click(IntroConfirmationPage.submit())

          .getUrl()
          .isExisting(IntroThankYouPagePage.signOut()).should.eventually.be.false;
      });
  });

  it('Given a logout url is not set, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    return helpers.openQuestionnaire('test_introduction.json', { includeLogoutUrl: false }).then(() => {
        return browser
          .getUrl()
          .isExisting(IntroductionPage.signOut()).should.eventually.be.false
          .click(IntroductionPage.getStarted())

          .getUrl()
          .getText(IntroInterstitialPage.saveSignOut()).should.eventually.contain('Save and complete later')
          .click(IntroInterstitialPage.submit())

          .getUrl()
          .getText(IntroConfirmationPage.saveSignOut()).should.eventually.contain('Save and complete later')
          .click(IntroConfirmationPage.submit())

          .getUrl()
          .isExisting(IntroductionPage.signOut()).should.eventually.be.false;
      });
  });

  it('Given a logout url is set, when I load the feedback page, then I see the sign out button', function() {
    return helpers.openQuestionnaire('test_numbers.json', { includeLogoutUrl: true }).then(() => {
        return browser
          .url(FeedbackForm.url())
          .getUrl()
          .isExisting(FeedbackForm.signOut()).should.eventually.be.true
          .getText(FeedbackForm.signOut()).should.eventually.contain('Sign out');
      });
  });

  it('Given a logout url is not set, when I load the feedback page, then there should be no sign out button', function() {
    return helpers.openQuestionnaire('test_numbers.json', { includeLogoutUrl: false }).then(() => {
        return browser
          .url(FeedbackForm.url())
          .getUrl()
          .isExisting(FeedbackForm.signOut()).should.eventually.be.false;
      });
  });

  it('Given a logout url is set and I load the feedback page, when I sign out, then I should be on the account service logged out page', function() {
    return helpers.openQuestionnaire('test_numbers.json', { includeLogoutUrl: true }).then(() => {
        return browser
          .url(FeedbackForm.url())
          .getUrl()
          .isExisting(FeedbackForm.signOut()).should.eventually.be.true
          .click(FeedbackForm.signOut())
          .getUrl().should.eventually.contain('http://localhost:8000');
      });
  });

});
