const helpers = require('../../../helpers');

describe('Component: Radio', function() {
  describe('Given I start a Mandatory Radio survey', function() {

    var RadioMandatoryPage = require('../../../pages/components/radio/mandatory/radio-mandatory.page');
    var RadioSummaryPage = require('../../../pages/components/radio/mandatory/summary.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_mandatory.json');
    });

    it('When I have selected a radio option, Then the selected option should be displayed in the summary', function() {
      return browser
       .click(RadioMandatoryPage.coffee())
       .click(RadioMandatoryPage.submit())
       .getUrl().should.eventually.contain(RadioSummaryPage.pageName)
       .getText(RadioSummaryPage.radioMandatoryAnswer()).should.eventually.contain('Coffee');
     });
  });

  describe('Given I start a Mandatory Radio Other survey', function() {

    var RadioMandatoryPage = require('../../../pages/components/radio/mandatory_with_mandatory_other/radio-mandatory.page');
    var RadioSummaryPage = require('../../../pages/components/radio/mandatory_with_mandatory_other/summary.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_mandatory_with_mandatory_other.json');
    });

    it('When I have selected a other text field, Then the selected option should be displayed in the summary', function() {
      return browser
       .click(RadioMandatoryPage.other())
       .setValue(RadioMandatoryPage.otherText(), 'Hello World')
       .click(RadioMandatoryPage.submit())
       .getUrl().should.eventually.contain(RadioSummaryPage.pageName)
       .getText(RadioSummaryPage.radioMandatoryAnswer()).should.eventually.contain('Hello World');
     });
  });

  describe('Given I start a Mandatory Radio Other Overridden Error survey ', function() {

    var RadioMandatoryPage = require('../../../pages/components/radio/mandatory_with_mandatory_other_overridden_error/radio-mandatory.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_mandatory_with_mandatory_other_overridden_error.json');
    });

    it('When I submit without any data in the other text field it should Then throw an overridden error', function() {
      return browser
        .click(RadioMandatoryPage.other())
        .click(RadioMandatoryPage.submit())
        .getText(RadioMandatoryPage.errorNumber(1)).should.eventually.contain('Test error message is overridden');
    });
  });


  describe('Given I start a Mandatory Radio Other survey ', function() {

    var RadioMandatoryPage = require('../../../pages/components/radio/mandatory_with_optional_other/radio-mandatory.page');
    var RadioSummaryPage = require('../../../pages/components/radio/mandatory_with_optional_other/summary.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_mandatory_with_optional_other.json');
    });

    it('When I submit without any data in the other text field is selected, Then the selected option should be displayed in the summary', function() {
      return browser
       .click(RadioMandatoryPage.submit())
       .getUrl().should.eventually.contain(RadioSummaryPage.pageName)
       .getText(RadioSummaryPage.radioMandatoryAnswer()).should.eventually.contain('No answer provided');
    });
  });


  describe('Given I start a Mandatory Radio Other Overridden error survey  ', function() {

    var RadioMandatoryPage = require('../../../pages/components/radio/mandatory_with_overridden_error/radio-mandatory.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_mandatory_with_overridden_error.json');
    });

    it('When I have submitted the page without any option, Then an overridden error is displayed', function() {
      return browser
       .click(RadioMandatoryPage.submit())
       .getText(RadioMandatoryPage.errorNumber(1)).should.eventually.contain('Test error message is overridden');
    });
  });

  describe('Given I start a Optional survey', function() {

    var RadioNonMandatoryPage = require('../../../pages/components/radio/optional/radio-non-mandatory.page');
    var RadioSummaryPage = require('../../../pages/components/radio/optional/summary.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_optional.json');
    });

    it('When I have selected no option, Then the selected option should be displayed in the summary', function() {
      return browser
       .click(RadioNonMandatoryPage.submit())
       .getUrl().should.eventually.contain(RadioSummaryPage.pageName)
       .getText(RadioSummaryPage.radioNonMandatoryAnswer()).should.eventually.contain('No answer provided');
    });
  });

  describe('Given I start a Optional Other Overridden error survey', function() {

    var RadioNonMandatoryPage = require('../../../pages/components/radio/optional_other_overridden_error_message_with_mandatory_other/radio-non-mandatory.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_optional_with_mandatory_other_overridden_error.json');
    });

    it('When I have submitted an other option with an empty text field, Then an overridden error is displayed', function() {
      return browser
        .click(RadioNonMandatoryPage.other())
        .click(RadioNonMandatoryPage.submit())
        .getText(RadioNonMandatoryPage.errorNumber(1)).should.eventually.contain('Test error message is overridden');
    });
  });


  describe('Given I Start a Optional Mandatory Other survey', function() {

    var RadioNonMandatoryPage = require('../../../pages/components/radio/optional_with_mandatory_other/radio-non-mandatory.page');
    var RadioSummaryPage = require('../../../pages/components/radio/optional_with_mandatory_other/summary.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_optional_with_mandatory_other.json');
    });

    it('When I submit data in the other text field it should be persisted and Then displayed on the summary', function() {
      return browser
       .click(RadioNonMandatoryPage.other())
       .setValue(RadioNonMandatoryPage.otherText(), 'Hello World')
       .click(RadioNonMandatoryPage.submit())
       .getUrl().should.eventually.contain(RadioSummaryPage.pageName)
       .getText(RadioSummaryPage.radioNonMandatoryAnswer()).should.eventually.contain('Hello World');
    });
  });

  describe('Given I start a Optional other Optional survey', function() {

    var RadioNonMandatoryPage = require('../../../pages/components/radio/optional_with_optional_other/radio-non-mandatory.page');
    var RadioSummaryPage = require('../../../pages/components/radio/optional_with_optional_other/summary.page');

    before(function() {
      return helpers.openQuestionnaire('test_radio_optional_with_optional_other.json');
    });

    it('When I select no option I should be directed to the summary and Then answer should be displayed on the summary', function() {
      return browser
       .click(RadioNonMandatoryPage.other())
       .click(RadioNonMandatoryPage.submit())
       .getText(RadioSummaryPage.radioNonMandatoryAnswer()).should.eventually.contain('No answer provided');
     });
  });

});
