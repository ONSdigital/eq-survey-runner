const helpers = require('../helpers');
const BreakfastPage = require('../pages/surveys/confirmation_page/breakfast.page.js');
const ConfirmationPage = require('../pages/surveys/confirmation_page/confirmation.page.js');

describe('Example Test', function() {

  it('Given I successfully complete a questionnaire, when I submit the page, then I should be prompted for confirmation to submit.', function() {
    return helpers.startQuestionnaire('test_final_confirmation.json').then(() => {
        return browser
          .setValue(BreakfastPage.answer(), 'Bacon')
          .click(BreakfastPage.submit())
          .getUrl().should.eventually.contain(ConfirmationPage.pageName);
    });
  });

    it('Given I successfully complete a questionnaire, when I confirm submit, then the submission is successful', function() {
    return helpers.startQuestionnaire('test_final_confirmation.json').then(() => {
        return browser
          .click(BreakfastPage.submit())
          .getUrl().should.eventually.contain(ConfirmationPage.pageName)
          .click(ConfirmationPage.submit())
          .getUrl().should.eventually.contain('thank-you');
    });
  });


});

