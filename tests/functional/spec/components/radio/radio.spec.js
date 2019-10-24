const helpers = require('../../../helpers');

describe('Component: Radio', function() {
  let browser;
  describe('Given I start a Mandatory Radio survey', function() {
    const RadioMandatoryPage = require('../../../generated_pages/radio_mandatory/radio-mandatory.page');
    const RadioSummaryPage = require('../../../generated_pages/radio_mandatory/summary.page');

    before(function() {
      helpers.openQuestionnaire('test_radio_mandatory.json').then(openBrowser => browser = openBrowser);
    });

    it('When I have selected a radio option, Then the selected option should be displayed in the summary', function() {
       $(RadioMandatoryPage.coffee()).click();
       $(RadioMandatoryPage.submit()).click();
       expect(browser.getUrl()).to.contain(RadioSummaryPage.pageName);
       expect($(RadioSummaryPage.radioMandatoryAnswer()).getText()).to.contain('Coffee');
     });
  });

  describe('Given I start a Mandatory Radio Other survey', function() {
    const RadioMandatoryPage = require('../../../generated_pages/radio_mandatory_with_optional_other/radio-mandatory.page');
    const RadioSummaryPage = require('../../../generated_pages/radio_mandatory_with_optional_other/summary.page');

    before(function() {
      helpers.openQuestionnaire('test_radio_mandatory_with_mandatory_other.json').then(openBrowser => browser = openBrowser);
    });

    it('When I have selected a other text field, Then the selected option should be displayed in the summary', function() {
       $(RadioMandatoryPage.other()).click();
       $(RadioMandatoryPage.otherDetail()).setValue('Hello World');
       $(RadioMandatoryPage.submit()).click();
       expect(browser.getUrl()).to.contain(RadioSummaryPage.pageName);
       expect($(RadioSummaryPage.radioMandatoryAnswer()).getText()).to.contain('Hello World');
     });
  });

  describe('Given I start a Mandatory Radio Other Overridden Error survey ', function() {
    const RadioMandatoryPage = require('../../../generated_pages/radio_mandatory_with_mandatory_other_overridden_error/radio-mandatory.page');

    before(function() {
      helpers.openQuestionnaire('test_radio_mandatory_with_mandatory_other_overridden_error.json').then(openBrowser => browser = openBrowser);
    });

    it('When I submit without any data in the other text field it should Then throw an overridden error', function() {
        $(RadioMandatoryPage.other()).click();
        $(RadioMandatoryPage.submit()).click();
        expect($(RadioMandatoryPage.errorNumber(1)).getText()).to.contain('Test error message is overridden');
    });
  });


  describe('Given I start a Mandatory Radio Other survey ', function() {
    const RadioMandatoryPage = require('../../../generated_pages/radio_mandatory_with_optional_other/radio-mandatory.page');
    const RadioSummaryPage = require('../../../generated_pages/radio_mandatory_with_optional_other/summary.page');

    before(function() {
      helpers.openQuestionnaire('test_radio_mandatory_with_optional_other.json').then(openBrowser => browser = openBrowser);
    });

    it('When I submit without any data in the other text field is selected, Then the selected option should be displayed in the summary', function() {
       $(RadioMandatoryPage.submit()).click();
       expect(browser.getUrl()).to.contain(RadioSummaryPage.pageName);
       expect($(RadioSummaryPage.radioMandatoryAnswer()).getText()).to.contain('No answer provided');
    });
  });


  describe('Given I start a Mandatory Radio Other Overridden error survey  ', function() {
    const RadioMandatoryPage = require('../../../generated_pages/radio_mandatory_with_overridden_error/radio-mandatory.page');

    before(function() {
      helpers.openQuestionnaire('test_radio_mandatory_with_overridden_error.json');
    });

    it('When I have submitted the page without any option, Then an overridden error is displayed', function() {
       $(RadioMandatoryPage.submit()).click();
       expect($(RadioMandatoryPage.errorNumber(1)).getText()).to.contain('Test error message is overridden');
    });
  });

  describe('Given I start a Optional survey', function() {
    const RadioNonMandatoryPage = require('../../../generated_pages/radio_optional/radio-non-mandatory.page');
    const RadioSummaryPage = require('../../../generated_pages/radio_optional/summary.page');

    before(function() {
      helpers.openQuestionnaire('test_radio_optional.json').then(openBrowser => browser = openBrowser);
    });

    it('When I have selected no option, Then the selected option should be displayed in the summary', function() {
       $(RadioNonMandatoryPage.submit()).click();
       expect(browser.getUrl()).to.contain(RadioSummaryPage.pageName);
       expect($(RadioSummaryPage.radioNonMandatoryAnswer()).getText()).to.contain('No answer provided');
    });
  });

  describe('Given I start a Optional Other Overridden error survey', function() {
    const RadioNonMandatoryPage = require('../../../generated_pages/radio_optional_with_mandatory_other_overridden_error/radio-non-mandatory.page');

    before(function() {
      helpers.openQuestionnaire('test_radio_optional_with_mandatory_other_overridden_error.json');
    });

    it('When I have submitted an other option with an empty text field, Then an overridden error is displayed', function() {
      $(RadioNonMandatoryPage.other()).click();
      $(RadioNonMandatoryPage.submit()).click();
      expect($(RadioNonMandatoryPage.errorNumber(1)).getText()).to.contain('Test error message is overridden');
    });
  });


  describe('Given I Start a Optional Mandatory Other survey', function() {
    const RadioNonMandatoryPage = require('../../../generated_pages/radio_optional_with_mandatory_other/radio-non-mandatory.page');
    const RadioSummaryPage = require('../../../generated_pages/radio_optional_with_mandatory_other/summary.page');

    before(function() {
      helpers.openQuestionnaire('test_radio_optional_with_mandatory_other.json').then(openBrowser => browser = openBrowser);
    });

    it('When I submit data in the other text field it should be persisted and Then displayed on the summary', function() {
      $(RadioNonMandatoryPage.other()).click();
      $(RadioNonMandatoryPage.otherDetail()).setValue('Hello World');
      $(RadioNonMandatoryPage.submit()).click();
      expect(browser.getUrl()).to.contain(RadioSummaryPage.pageName);
      expect($(RadioSummaryPage.radioNonMandatoryAnswer()).getText()).to.contain('Hello World');
    });
  });
});
