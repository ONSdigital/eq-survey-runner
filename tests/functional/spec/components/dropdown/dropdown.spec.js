const helpers = require('../../../helpers');

describe('Component: Dropdown', function() {
  //Mandatory
  describe('Given I start a Mandatory Dropdown survey', function() {

    const DropdownMandatoryPage = require('../../../pages/components/dropdown/mandatory/dropdown-mandatory.page');
    const DropdownSummaryPage = require('../../../pages/components/dropdown/mandatory/summary.page');
    const schema = 'test_dropdown_mandatory.json';

    it('When I have selected a dropdown option, Then the selected option should be displayed in the summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .selectByValue(DropdownMandatoryPage.answer(), "Rugby is better!")
            .click(DropdownMandatoryPage.submit())
            .getText(DropdownSummaryPage.dropdownMandatoryAnswer()).should.eventually.contain("Rugby is better!");
        });
    });

    it('When I have not selected a dropdown option and click Continue, Then the default error message should be displayed', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .click(DropdownMandatoryPage.submit())
            .getText(DropdownMandatoryPage.errorNumber(1)).should.eventually.contain("Select an answer to continue.");
        });
    });

    it('When I have selected a dropdown option and I try to select a default (disabled) dropdown option, Then the already selected option should be displayed in summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .selectByValue(DropdownMandatoryPage.answer(), "Liverpool")
            .selectByValue(DropdownMandatoryPage.answer(), "")
            .click(DropdownMandatoryPage.submit())
            .getText(DropdownSummaryPage.dropdownMandatoryAnswer()).should.eventually.contain("Liverpool");
        });
    });

    it('When I click the dropdown label, Then the dropdown should be focused', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .click(DropdownMandatoryPage.answerLabel())
            .hasFocus(DropdownMandatoryPage.answer()).should.eventually.be.true;
        });
    });

    it('When I\'m on the summary page and I click Edit then Continue, Then the answer on the summary page should be unchanged', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .selectByValue(DropdownMandatoryPage.answer(), "Rugby is better!")
            .click(DropdownMandatoryPage.submit())
            .getText(DropdownSummaryPage.dropdownMandatoryAnswer()).should.eventually.contain("Rugby is better!")
            .click(DropdownSummaryPage.dropdownMandatoryAnswerEdit())
            .click(DropdownMandatoryPage.submit())
            .getText(DropdownSummaryPage.dropdownMandatoryAnswer()).should.eventually.contain("Rugby is better!");
        });
    });

    it('When I\'m on the summary page and I click Edit and change the answer, Then the newly selected answer should be displayed in the summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .selectByValue(DropdownMandatoryPage.answer(), "Rugby is better!")
            .click(DropdownMandatoryPage.submit())
            .getText(DropdownSummaryPage.dropdownMandatoryAnswer()).should.eventually.contain("Rugby is better!")
            .click(DropdownSummaryPage.dropdownMandatoryAnswerEdit())
            .click(DropdownMandatoryPage.submit())
            .getText(DropdownSummaryPage.dropdownMandatoryAnswer()).should.eventually.contain("Rugby is better!")
            .click(DropdownSummaryPage.dropdownMandatoryAnswerEdit())
            .selectByValue(DropdownMandatoryPage.answer(), "Liverpool")
            .click(DropdownMandatoryPage.submit())
            .getText(DropdownSummaryPage.dropdownMandatoryAnswer()).should.eventually.contain("Liverpool");
        });
    });
  });

  describe('Given I start a Mandatory With Overridden Error Dropdown survey', function() {

    const DropdownMandatoryPage = require('../../../pages/components/dropdown/mandatory_with_overridden_error/dropdown-mandatory-with-overridden-error.page');

    before(function() {
      return helpers.openQuestionnaire('test_dropdown_mandatory_with_overridden_error.json');
    });

    it('When I have not selected a dropdown option and click Continue, Then the overridden error message should be displayed', function() {
      return browser
        .click(DropdownMandatoryPage.submit())
        .getText(DropdownMandatoryPage.errorNumber(1)).should.eventually.contain("Overridden test error message.");
    });
  });

  //Optional
  describe('Given I start a Optional Dropdown survey', function() {

    const DropdownOptionalPage = require('../../../pages/components/dropdown/optional/dropdown-optional.page');
    const DropdownSummaryPage = require('../../../pages/components/dropdown/optional/summary.page');
    const schema = 'test_dropdown_optional.json';

    it('When I have not selected a dropdown option, Then the summary should display "No answer provided"', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .click(DropdownOptionalPage.submit())
            .getText(DropdownSummaryPage.dropdownOptionalAnswer()).should.eventually.contain("No answer provided");
        });
    });

    it('When I have selected a dropdown option, Then the selected option should be displayed in the summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .selectByValue(DropdownOptionalPage.answer(), "Rugby is better!")
            .click(DropdownOptionalPage.submit())
            .getText(DropdownSummaryPage.dropdownOptionalAnswer()).should.eventually.contain("Rugby is better!");
        });
    });

    it('When I have selected a dropdown option and I reselect the default option (Select an answer), Then the summary should display "No answer provided"', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .selectByValue(DropdownOptionalPage.answer(), "Chelsea")
            .click(DropdownOptionalPage.submit())
            .getText(DropdownSummaryPage.dropdownOptionalAnswer()).should.eventually.contain("Chelsea")
            .click(DropdownSummaryPage.dropdownOptionalAnswerEdit())
            .selectByValue(DropdownOptionalPage.answer(), "")
            .click(DropdownOptionalPage.submit())
            .getText(DropdownSummaryPage.dropdownOptionalAnswer()).should.eventually.contain("No answer provided");
        });
    });
  });

});
