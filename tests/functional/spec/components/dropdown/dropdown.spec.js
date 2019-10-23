const helpers = require('../../../helpers');

describe('Component: Dropdown', function() {
  //Mandatory
  describe('Given I start a Mandatory Dropdown survey', function() {

    const DropdownMandatoryPage = require('../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page');
    const DropdownSummaryPage = require('../../../generated_pages/dropdown_mandatory/summary.page');
    const schema = 'test_dropdown_mandatory.json';

    it('When I have selected a dropdown option, Then the selected option should be displayed in the summary', function() {
      helpers.openQuestionnaire(schema);
      $(DropdownMandatoryPage.answer()).selectByAttribute('value', "Rugby is better!");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
    });

    it('When I have not selected a dropdown option and click Continue, Then the default error message should be displayed', function() {
      browser = helpers.openQuestionnaire(schema);
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatoryPage.errorNumber(1)).getText()).to.contain("Select an answer to continue.");
    });

    it('When I have selected a dropdown option and I try to select a default (disabled) dropdown option, Then the already selected option should be displayed in summary', function() {
      helpers.openQuestionnaire(schema);
      $(DropdownMandatoryPage.answer()).selectByAttribute('value', "Liverpool");
      $(DropdownMandatoryPage.answer()).selectByAttribute('value', "");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownMandatoryAnswer()).getText()).to.contain("Liverpool");
    });

    it('When I click the dropdown label, Then the dropdown should be focused', function() {
      browser = helpers.openQuestionnaire(schema);
      $(DropdownMandatoryPage.answerLabel()).click();
      expect($(DropdownMandatoryPage.answer()).isFocused()).to.be.true;
    });

    it('When I\'m on the summary page and I click Edit then Continue, Then the answer on the summary page should be unchanged', function() {
      helpers.openQuestionnaire(schema);
      $(DropdownMandatoryPage.answer()).selectByAttribute('value', "Rugby is better!");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
      $(DropdownSummaryPage.dropdownMandatoryAnswerEdit()).click();
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
    });

    it('When I\'m on the summary page and I click Edit and change the answer, Then the newly selected answer should be displayed in the summary', function() {
      helpers.openQuestionnaire(schema);
      $(DropdownMandatoryPage.answer()).selectByAttribute('value', "Rugby is better!");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
      $(DropdownSummaryPage.dropdownMandatoryAnswerEdit()).click();
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
      $(DropdownSummaryPage.dropdownMandatoryAnswerEdit()).click();
      $(DropdownMandatoryPage.answer()).selectByAttribute('value', "Liverpool");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownMandatoryAnswer()).getText()).to.contain("Liverpool");
    });
  });

  describe('Given I start a Mandatory With Overridden Error Dropdown survey', function() {

    const DropdownMandatoryPage = require('../../../generated_pages/dropdown_mandatory_with_overridden_error/dropdown-mandatory-with-overridden-error.page');

    before(function() {
      helpers.openQuestionnaire('test_dropdown_mandatory_with_overridden_error.json');
    });

    it('When I have not selected a dropdown option and click Continue, Then the overridden error message should be displayed', function() {
        $(DropdownMandatoryPage.submit()).click();
        expect($(DropdownMandatoryPage.errorNumber(1)).getText()).to.contain("Overridden test error message.");
    });
  });

  //Optional
  describe('Given I start a Optional Dropdown survey', function() {

    const DropdownOptionalPage = require('../../../generated_pages/dropdown_optional/dropdown-optional.page');
    const DropdownSummaryPage = require('../../../generated_pages/dropdown_optional/summary.page');
    const schema = 'test_dropdown_optional.json';

    it('When I have not selected a dropdown option, Then the summary should display "No answer provided"', function() {
      helpers.openQuestionnaire(schema);
      $(DropdownOptionalPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownOptionalAnswer()).getText()).to.contain("No answer provided");
    });

    it('When I have selected a dropdown option, Then the selected option should be displayed in the summary', function() {
      helpers.openQuestionnaire(schema);
      $(DropdownOptionalPage.answer()).selectByAttribute('value', "Rugby is better!");
      $(DropdownOptionalPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownOptionalAnswer()).getText()).to.contain("Rugby is better!");
    });

    it('When I have selected a dropdown option and I reselect the default option (Select an answer), Then the summary should display "No answer provided"', function() {
      helpers.openQuestionnaire(schema);
      $(DropdownOptionalPage.answer()).selectByAttribute('value', "Chelsea");
      $(DropdownOptionalPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownOptionalAnswer()).getText()).to.contain("Chelsea");
      $(DropdownSummaryPage.dropdownOptionalAnswerEdit()).click();
      $(DropdownOptionalPage.answer()).selectByAttribute('value', "");
      $(DropdownOptionalPage.submit()).click();
      expect($(DropdownSummaryPage.dropdownOptionalAnswer()).getText()).to.contain("No answer provided");
    });
  });

});
