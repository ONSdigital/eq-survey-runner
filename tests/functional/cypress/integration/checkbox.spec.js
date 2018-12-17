import {openQuestionnaire, getToken} from '../helpers/helpers'

const MandatoryCheckboxPage = require('../../generated_pages/checkbox/mandatory-checkbox.page');
const NonMandatoryCheckboxPage = require('../../generated_pages/checkbox/non-mandatory-checkbox.page');
const SummaryPage = require('../../generated_pages/checkbox/summary.page');


describe('Checkbox with "other" option', function() {

  const checkbox_schema = 'test_checkbox.json';

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible.', function() {
    openQuestionnaire(checkbox_schema)
      .get(MandatoryCheckboxPage.otherLabel()).should('contain', 'Choose any other topping')
      .get(MandatoryCheckboxPage.other()).click()
      .get(MandatoryCheckboxPage.otherDetail()).should('be.visible')
    })

  it('Given a mandatory checkbox answer, When I select the other option, leave the input field empty and submit, Then an error should be displayed.', function() {
    openQuestionnaire(checkbox_schema)
        .get(MandatoryCheckboxPage.other()).click()
        .get(MandatoryCheckboxPage.submit()).click()
        .get(MandatoryCheckboxPage.error()).should('exist')
  });
    it('Given a mandatory checkbox answer, when there is an error on the page for other field and I enter valid value and submit page, then the error is cleared and I navigate to next page.s', function() {
      openQuestionnaire(checkbox_schema)
          .get(MandatoryCheckboxPage.other()).click()
          .get(MandatoryCheckboxPage.submit()).click()
          .get(MandatoryCheckboxPage.error()).should('exist')
          .get(MandatoryCheckboxPage.otherDetail()).type('Other Text')
          .get(MandatoryCheckboxPage.submit()).click()
          .url().should('contain', NonMandatoryCheckboxPage.pageName);
    });

    it('Given a non-mandatory checkbox answer, when the user does not select an option, then "No answer provided" should be displayed on the summary screen', function() {
      openQuestionnaire(checkbox_schema)
          .get(MandatoryCheckboxPage.other()).click()
          .get(MandatoryCheckboxPage.otherDetail()).type('Other value')
          .get(MandatoryCheckboxPage.submit()).click()
          .get(NonMandatoryCheckboxPage.submit()).click()
          .get(SummaryPage.nonMandatoryCheckboxAnswer()).should('contain', 'No answer provided');
    });

      it('Given a non-mandatory checkbox answer, when the user selects Other but does not supply a value, then "Other" should be displayed on the summary screen', function() {
        openQuestionnaire(checkbox_schema)
            .get(MandatoryCheckboxPage.other()).click()
            .get(MandatoryCheckboxPage.otherDetail()).type('Other value')
            .get(MandatoryCheckboxPage.submit()).click()
            .get(NonMandatoryCheckboxPage.other()).click()
            .get(NonMandatoryCheckboxPage.submit()).click()
            .get(SummaryPage.nonMandatoryCheckboxAnswer()).should('contain', 'Other');
      });

      it('Given a non-mandatory checkbox answer, when the user selects Other and supplies a value, then the supplied value should be displayed on the summary screen', function() {
        openQuestionnaire(checkbox_schema)
            .get(MandatoryCheckboxPage.other()).click()
            .get(MandatoryCheckboxPage.otherDetail()).type('Other value')
            .get(MandatoryCheckboxPage.submit()).click()
            .get(NonMandatoryCheckboxPage.other()).click()
            .get(NonMandatoryCheckboxPage.otherDetail()).type('The other value')
            .get(NonMandatoryCheckboxPage.submit()).click()
            .get(SummaryPage.nonMandatoryCheckboxAnswer()).should('contain', 'The other value');
      });

      it('Given I have previously added text in other textfield and saved, when I uncheck other options and select a different checkbox as answer, then the text entered in other field must be wiped.', function() {
        openQuestionnaire(checkbox_schema)
            .get(MandatoryCheckboxPage.other()).click()
            .get(MandatoryCheckboxPage.otherDetail()).type('Other value')
            .get(MandatoryCheckboxPage.submit()).click()
            .get(NonMandatoryCheckboxPage.previous()).click()
            .get(MandatoryCheckboxPage.other()).click()
            .get(MandatoryCheckboxPage.cheese()).click()
            .get(MandatoryCheckboxPage.submit()).click()
            .get(NonMandatoryCheckboxPage.previous()).click()
            .get(MandatoryCheckboxPage.other()).click()
            .get(MandatoryCheckboxPage.otherDetail()).invoke('text').should('equal', '')
      });

      it('Given a mandatory checkbox answer, when the user selects only one option, then the answer should not be displayed as a list on the summary screen', function() {
        openQuestionnaire(checkbox_schema)
            .get(MandatoryCheckboxPage.ham()).click()
            .get(MandatoryCheckboxPage.submit()).click()
            .get(NonMandatoryCheckboxPage.submit()).click()
            .get(SummaryPage.mandatoryCheckboxAnswer()).should('not.contain', 'li')
      });

        it('Given a mandatory checkbox answer, when the user selects more than one option, then the answer should be displayed as a list on the summary screen', function() {
        openQuestionnaire(checkbox_schema)
            .get(MandatoryCheckboxPage.ham()).click()
            .get(MandatoryCheckboxPage.cheese()).click()
            .get(MandatoryCheckboxPage.submit()).click()
            .get(NonMandatoryCheckboxPage.submit()).click()
            .get(SummaryPage.mandatoryCheckboxAnswer()).find('li').then(result => result.length).should('equal', 2)
        });

});
