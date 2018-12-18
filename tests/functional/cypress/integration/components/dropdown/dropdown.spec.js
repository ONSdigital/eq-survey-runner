import {openQuestionnaire} from ../../../helpers/helpers.js

describe('Component: Dropdown', function() {
  //Mandatory
  describe('Given I start a Mandatory Dropdown survey', function() {

    const DropdownMandatoryPage = require('../../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page');
    const DropdownSummaryPage = require('../../../../generated_pages/dropdown_mandatory/summary.page');
    const schema = 'test_dropdown_mandatory.json';

    it('When I have selected a dropdown option, Then the selected option should be displayed in the summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownMandatoryPage.answer()).select("Rugby is better!")
            .get(DropdownMandatoryPage.submit()).click()
            .get(DropdownSummaryPage.dropdownMandatoryAnswer()).stripText().should('contain', "Rugby is better!");
        });
    });

    it('When I have not selected a dropdown option and click Continue, Then the default error message should be displayed', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownMandatoryPage.submit()).click()
            .get(DropdownMandatoryPage.errorNumber(1)).stripText().should('contain', "Select an answer to continue.");
        });
    });

    it('When I have selected a dropdown option and I try to select a default (disabled) dropdown option, Then the already selected option should be displayed in summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownMandatoryPage.answer()).select("Liverpool")
            .get(DropdownMandatoryPage.answer()).select("")
            .get(DropdownMandatoryPage.submit()).click()
            .get(DropdownSummaryPage.dropdownMandatoryAnswer()).stripText().should('contain', "Liverpool");
        });
    });

    it('When I click the dropdown label, Then the dropdown should be focused', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownMandatoryPage.answerLabel()).click()
            .focused().should('match', DropdownMandatoryPage.answer())
        });
    });

    it('When I\'m on the summary page and I click Edit then Continue, Then the answer on the summary page should be unchanged', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownMandatoryPage.answer()).select("Rugby is better!")
            .get(DropdownMandatoryPage.submit()).click()
            .get(DropdownSummaryPage.dropdownMandatoryAnswer()).stripText().should('contain', "Rugby is better!")
            .get(DropdownSummaryPage.dropdownMandatoryAnswerEdit()).click()
            .get(DropdownMandatoryPage.submit()).click()
            .get(DropdownSummaryPage.dropdownMandatoryAnswer()).stripText().should('contain', "Rugby is better!");
        });
    });

    it('When I\'m on the summary page and I click Edit and change the answer, Then the newly selected answer should be displayed in the summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownMandatoryPage.answer()).select("Rugby is better!")
            .get(DropdownMandatoryPage.submit()).click()
            .get(DropdownSummaryPage.dropdownMandatoryAnswer()).stripText().should('contain', "Rugby is better!")
            .get(DropdownSummaryPage.dropdownMandatoryAnswerEdit()).click()
            .get(DropdownMandatoryPage.submit()).click()
            .get(DropdownSummaryPage.dropdownMandatoryAnswer()).stripText().should('contain', "Rugby is better!")
            .get(DropdownSummaryPage.dropdownMandatoryAnswerEdit()).click()
            .get(DropdownMandatoryPage.answer()).select("Liverpool")
            .get(DropdownMandatoryPage.submit()).click()
            .get(DropdownSummaryPage.dropdownMandatoryAnswer()).stripText().should('contain', "Liverpool");
        });
    });
  });

  describe('Given I start a Mandatory With Overridden Error Dropdown survey', function() {

    const DropdownMandatoryPage = require('../../../../generated_pages/dropdown_mandatory_with_overridden_error/dropdown-mandatory-with-overridden-error.page');

    before(function() {
      return helpers.openQuestionnaire('test_dropdown_mandatory_with_overridden_error.json');
    });

    it('When I have not selected a dropdown option and click Continue, Then the overridden error message should be displayed', function() {
              .get(DropdownMandatoryPage.submit()).click()
        .get(DropdownMandatoryPage.errorNumber(1)).stripText().should('contain', "Overridden test error message.");
    });
  });

  //Optional
  describe('Given I start a Optional Dropdown survey', function() {

    const DropdownOptionalPage = require('../../../../generated_pages/dropdown_optional/dropdown-optional.page');
    const DropdownSummaryPage = require('../../../../generated_pages/dropdown_optional/summary.page');
    const schema = 'test_dropdown_optional.json';

    it('When I have not selected a dropdown option, Then the summary should display "No answer provided"', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownOptionalPage.submit()).click()
            .get(DropdownSummaryPage.dropdownOptionalAnswer()).stripText().should('contain', "No answer provided");
        });
    });

    it('When I have selected a dropdown option, Then the selected option should be displayed in the summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownOptionalPage.answer()).select("Rugby is better!")
            .get(DropdownOptionalPage.submit()).click()
            .get(DropdownSummaryPage.dropdownOptionalAnswer()).stripText().should('contain', "Rugby is better!");
        });
    });

    it('When I have selected a dropdown option and I reselect the default option (Select an answer), Then the summary should display "No answer provided"', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
                      .get(DropdownOptionalPage.answer()).select("Chelsea")
            .get(DropdownOptionalPage.submit()).click()
            .get(DropdownSummaryPage.dropdownOptionalAnswer()).stripText().should('contain', "Chelsea")
            .get(DropdownSummaryPage.dropdownOptionalAnswerEdit()).click()
            .get(DropdownOptionalPage.answer()).select("")
            .get(DropdownOptionalPage.submit()).click()
            .get(DropdownSummaryPage.dropdownOptionalAnswer()).stripText().should('contain', "No answer provided");
        });
    });
  });

});
