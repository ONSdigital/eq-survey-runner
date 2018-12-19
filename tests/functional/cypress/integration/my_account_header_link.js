import {openQuestionnaire} from '../helpers/helpers.js'

const IntroductionPage = require('../../generated_pages/introduction/introduction.page');
const QuestionPage = require('../../base_pages/generic.page');
const SummaryPage = require('../../base_pages/summary.page');
const ThankYouPage = require('../../base_pages/thank-you.page');

describe('My Account header link', function() {
  beforeEach(() => {
    openQuestionnaire('test_introduction.json')
  })

  it('Given I start a survey, When I go through every page then I should see the "My account" button on each page', function() {
    cy
      .url().should('contain', 'introduction')
      .get(IntroductionPage.myAccountLink()).stripText().should('contain', 'My account')
      .get(IntroductionPage.getStarted()).click()
      .url().should('contain', 'general-business-information-completed')
      .get(QuestionPage.myAccountLink()).stripText().should('contain', 'My account')
      .get(QuestionPage.submit()).click()
      .url().should('contain', 'confirmation')
      .get(SummaryPage.myAccountLink()).stripText().should('contain', 'My account')
      .get(SummaryPage.submit()).click()
      .url().should('contain', 'thank-you')
      .get(ThankYouPage.myAccountLink()).stripText().should('contain', 'My account');
  });
});
