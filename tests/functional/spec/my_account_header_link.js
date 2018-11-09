const helpers = require('../helpers');

const IntroductionPage = require('../base_pages/introduction.page');
const QuestionPage = require('../base_pages/generic.page');
const SummaryPage = require('../base_pages/summary.page');
const ThankYouPage = require('../base_pages/thank-you.page');

describe('Introduction page', function() {

  it('Given I start a survey, When I go through every page then I should see the "My account" button on each page', function() {
    return helpers.openQuestionnaire('test_introduction.json').then(() => {
      return browser
        .getUrl().should.eventually.contain('introduction')
        .getText(IntroductionPage.myAccountLink()).should.eventually.contain('My account')
        .click(IntroductionPage.getStarted())
        .getUrl().should.eventually.contain('general-business-information-completed')
        .getText(QuestionPage.myAccountLink()).should.eventually.contain('My account')
        .click(QuestionPage.submit())
        .getUrl().should.eventually.contain('confirmation')
        .getText(SummaryPage.myAccountLink()).should.eventually.contain('My account')
        .click(SummaryPage.submit())
        .getUrl().should.eventually.contain('thank-you')
        .getText(ThankYouPage.myAccountLink()).should.eventually.contain('My account');
    });
  });
});
