const utilities = require('../utilities');
const SetMinMax = require('../generated_pages/numbers/set-min-max-block.page.js');
const TestMinMax = require('../generated_pages/numbers/test-min-max-block.page.js');
const SummaryPage = require('../generated_pages/numbers/summary.page');

const IntroductionPage = require('../generated_pages/introduction/introduction.page');
const IntroInterstitialPage = require('../generated_pages/introduction/general-business-information-completed.page');
const IntroConfirmationPage = require('../generated_pages/introduction/confirmation.page');
const IntroThankYouPagePage = require('../base_pages/thank-you.page');

describe('SaveSignOut', function() {
  const responseId = utilities.getRandomString(16);

  it('Given I am completing a survey, when I select save and complete later, then I am redirected to sign out page and my session is cleared', function() {
    browser.openQuestionnaire('test_numbers.json', { userId: 'test_user', responseId: responseId } );
    $(SetMinMax.setMinimum()).setValue('10');
    $(SetMinMax.setMaximum()).setValue('1020');
    $(SetMinMax.submit()).click();
    $(TestMinMax.saveSignOut()).click();

    expect(browser.getUrl()).to.contain('localhost');

    browser.back();

    expect($('body').getHTML()).to.contain('Your session has expired');
  });

  it('Given I have started a questionnaire, when I return to the questionnaire, then I am returned to the page I was on and can then complete the survey', function() {
    browser.openQuestionnaire('test_numbers.json', { userId: 'test_user', responseId: responseId } );

    $(TestMinMax.testRange()).setValue('10');
    $(TestMinMax.testMin()).setValue('123');
    $(TestMinMax.testMax()).setValue('1000');
    $(TestMinMax.testPercent()).setValue('100');
    $(TestMinMax.submit()).click();

    $(SummaryPage.submit()).click();
    expect(browser.getUrl()).to.contain('thank-you');
  });

  it('Given a logout url is set, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    browser.openQuestionnaire('test_introduction.json', { includeLogoutUrl: true });

    expect($(IntroductionPage.signOut()).getText()).to.contain('Sign out');
    $(IntroductionPage.getStarted()).click();

    expect($(IntroInterstitialPage.saveSignOut()).getText()).to.contain('Save and sign out');
    $(IntroInterstitialPage.submit()).click();

    expect($(IntroConfirmationPage.saveSignOut()).getText()).to.contain('Save and sign out');
    $(IntroConfirmationPage.submit()).click();

    expect($(IntroThankYouPagePage.signOut()).isExisting()).to.be.false;
  });

  it('Given a logout url is not set, when I navigate the questionnaire, then I see the correct sign out buttons', function() {
    browser.openQuestionnaire('test_introduction.json', { includeLogoutUrl: false });

    expect($(IntroductionPage.signOut()).isExisting()).to.be.false;
    $(IntroductionPage.getStarted()).click();

    expect($(IntroInterstitialPage.saveSignOut()).getText()).to.contain('Save and complete later');
    $(IntroInterstitialPage.submit()).click();

    expect($(IntroConfirmationPage.saveSignOut()).getText()).to.contain('Save and complete later');
    $(IntroConfirmationPage.submit()).click();

    expect($(IntroductionPage.signOut()).isExisting()).to.be.false;
  });
});
