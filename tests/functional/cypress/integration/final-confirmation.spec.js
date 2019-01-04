import {startQuestionnaire} from '../helpers/helpers.js';
const BreakfastPage = require('../../generated_pages/final_confirmation/breakfast.page.js');
const ConfirmationPage = require('../../generated_pages/final_confirmation/confirmation.page.js');

describe('Confirmation Page', function() {

  beforeEach(() => {
    startQuestionnaire('test_final_confirmation.json');
  });

  it('Given I successfully complete a questionnaire, when I submit the page, then I should be prompted for confirmation to submit.', function() {
    cy
      .get(BreakfastPage.answer()).type('Bacon')
      .get(BreakfastPage.submit()).click()
      .url().should('contain', ConfirmationPage.pageName);
  });

  it('Given I successfully complete a questionnaire, when I confirm submit, then the submission is successful', function() {
    cy
      .get(BreakfastPage.submit()).click()
      .url().should('contain', ConfirmationPage.pageName)
      .get(ConfirmationPage.submit()).click()
      .url().should('contain', 'thank-you');
  });


});

