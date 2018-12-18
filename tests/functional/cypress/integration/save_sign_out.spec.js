import {openQuestionnaire} from ../helpers/helpers.js
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

  const collectionId = helpers.getRandomString(10);

  it('Given I am completing a survey, when I select save and complete later, then I am redirected to sign out page and my session is cleared', function() {
    openQuestionnaire('test_numbers.json', { userId: 'test_user', collectionId: collectionId })
                  .get(SetMinMax.setMinimum()).type('10')
          .get(SetMinMax.setMaximum()).type('1020')
          .get(SetMinMax.submit()).click()
          .get(TestMinMax.saveSignOut()).click()
          .url().should('contain', 'localhost')
          .back()
          .getSource().should.eventually.contain('Your session has expired');
      });
  });

  it('Given I have started a questionnaire, when I return to the questionnaire, then I am returned to the page I was on and can then complete the survey', function() {
    openQuestionnaire('test_numbers.json', { userId: 'test_user', collectionId: collectionId })
                  .url().should('contain', TestMinMax.pageName)
          .get(TestMinMax.testRange()).type('10')
          .get(TestMinMax.testMin()).type('123')
          .get(TestMinMax.testMax()).type('1000')
          .get(TestMinMax.testPercent()).type('100')
          .get(TestMinMax.submit()).click()
          .url().should('contain', SummaryPage.pageName)
          .get(SummaryPage.submit()).click()
          .url().should('contain', 'thank-you');
      });
  });

  it('Given a logout url is set, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    openQuestionnaire('test_introduction.json', { includeLogoutUrl: true })
                  .url().should('contain', IntroductionPage.pageName)
          .get(IntroductionPage.signOut()).stripText().should('contain', 'Sign out')
          .get(IntroductionPage.getStarted()).click()

          .url().should('contain', IntroInterstitialPage.pageName)
          .get(IntroInterstitialPage.saveSignOut()).stripText().should('contain', 'Save and sign out')
          .get(IntroInterstitialPage.submit()).click()

          .url().should('contain', IntroConfirmationPage.pageName)
          .get(IntroConfirmationPage.saveSignOut()).stripText().should('contain', 'Save and sign out')
          .get(IntroConfirmationPage.submit()).click()

          .url().should('contain', IntroThankYouPagePage.pageName)
          .get(IntroThankYouPagePage.signOut()).stripText().should('contain', 'Sign out');
      });
  });

  it('Given a logout url is not set, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    openQuestionnaire('test_introduction.json', { includeLogoutUrl: false })
                  .url().should('contain', IntroductionPage.pageName)
          .get(IntroductionPage.signOut()).should('not.exist')
          .get(IntroductionPage.getStarted()).click()

          .url().should('contain', IntroInterstitialPage.pageName)
          .get(IntroInterstitialPage.saveSignOut()).stripText().should('contain', 'Save and complete later')
          .get(IntroInterstitialPage.submit()).click()

          .url().should('contain', IntroConfirmationPage.pageName)
          .get(IntroConfirmationPage.saveSignOut()).stripText().should('contain', 'Save and complete later')
          .get(IntroConfirmationPage.submit()).click()

          .url().should('contain', IntroThankYouPagePage.pageName)
          .get(IntroductionPage.signOut()).should('not.exist');
      });
  });

  it('Given I am on a northern ireland themed survey, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    openQuestionnaire('test_theme_northernireland.json', { includeLogoutUrl: true })
                  .url().should('contain', NIRadioPage.pageName)
          .get(NIRadioPage.saveSignOut()).stripText().should('contain', 'Save and sign out')
          .get(NIRadioPage.submit()).click()
          .url().should('contain', NISummaryPage.pageName)
          .get(NISummaryPage.saveSignOut()).stripText().should('contain', 'Save and sign out')
          .get(NISummaryPage.submit()).click()
          .url().should('contain', NIThankYouPage.pageName)
          .get(NIThankYouPage.signOut()).stripText().should('contain', 'Sign out')
          .get(NIThankYouPage.viewSubmitted()).click()
          .url().should('contain', 'view-submission')
          .get(NIViewSubmissionPage.signOut()).stripText().should('contain', 'Sign out');
      });
  });

  it('Given I am on a social themed survey, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    openQuestionnaire('test_theme_social.json', { includeLogoutUrl: false } )
                  .url().should('contain', SocialRadioPage.pageName)
          .get(SocialRadioPage.saveSignOut()).stripText().should('contain', 'Save and complete later')
          .get(SocialRadioPage.submit()).click()
          .url().should('contain', SocialSummaryPage.pageName)
          .get(SocialSummaryPage.saveSignOut()).stripText().should('contain', 'Save and complete later')
          .get(SocialSummaryPage.submit()).click()
          .url().should('contain', SocialThankYouPage.pageName)
          .get(SocialThankYouPage.signOut()).should('not.exist')
          .get(SocialThankYouPage.viewSubmitted()).click()
          .url().should('contain', 'view-submission')
          .get(SocialViewSubmissionPage.signOut()).should('not.exist');
      });
  });

  it('Given a logout url is set, when I load the feedback page, then I see the sign out button', function() {
    openQuestionnaire('test_numbers.json', { includeLogoutUrl: true })
                  .url(FeedbackForm.url())
          .url().should('contain', 'feedback')
          .get(FeedbackForm.signOut()).should('exist')
          .get(FeedbackForm.signOut()).stripText().should('contain', 'Sign out');
      });
  });

  it('Given a logout url is not set, when I load the feedback page, then there should be no sign out button', function() {
    openQuestionnaire('test_numbers.json', { includeLogoutUrl: false })
                  .url(FeedbackForm.url())
          .url().should('contain', 'feedback')
          .get(FeedbackForm.signOut()).should('not.exist');
      });
  });

  it('Given a logout url is set and I load the feedback page, when I sign out, then I should be on the account service logged out page', function() {
    openQuestionnaire('test_numbers.json', { includeLogoutUrl: true })
                  .url(FeedbackForm.url())
          .url().should('contain', 'feedback')
          .get(FeedbackForm.signOut()).should('exist')
          .get(FeedbackForm.signOut()).click()
          .url().should('contain', 'http://localhost:8000');
      });
  });

});
