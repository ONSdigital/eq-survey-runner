import {openQuestionnaire} from '../../../helpers/helpers.js'

describe('Component: Radio', function() {
  describe('Given I start a Mandatory Radio survey', function() {

    var RadioMandatoryPage = require('../../../../generated_pages/radio_mandatory/radio-mandatory.page');
    var RadioSummaryPage = require('../../../../generated_pages/radio_mandatory/summary.page');

    beforeEach(function() {
      openQuestionnaire('test_radio_mandatory.json');
    });

    it('When I have selected a radio option, Then the selected option should be displayed in the summary', function() {
      cy
       .get(RadioMandatoryPage.coffee()).click()
       .get(RadioMandatoryPage.submit()).click()
       .url().should('contain', RadioSummaryPage.pageName)
       .get(RadioSummaryPage.radioMandatoryAnswer()).stripText().should('contain', 'Coffee');
     });
  });

  describe('Given I start a Mandatory Radio Other survey', function() {

    var RadioMandatoryPage = require('../../../../generated_pages/radio_mandatory_with_mandatory_other/radio-mandatory.page');
    var RadioSummaryPage = require('../../../../generated_pages/radio_mandatory_with_mandatory_other/summary.page');

    beforeEach(function() {
      openQuestionnaire('test_radio_mandatory_with_mandatory_other.json');
    });

    it('When I have selected a other text field, Then the selected option should be displayed in the summary', function() {
      cy
       .get(RadioMandatoryPage.other()).click()
       .get(RadioMandatoryPage.otherDetail())
       .type('Hello World')
       .get(RadioMandatoryPage.submit()).click()
       .url().should('contain', RadioSummaryPage.pageName)
       .get(RadioSummaryPage.radioMandatoryAnswer()).stripText().should('contain', 'Hello World');
     });
  });

  describe('Given I start a Mandatory Radio Other Overridden Error survey ', function() {

    var RadioMandatoryPage = require('../../../../generated_pages/radio_mandatory_with_mandatory_other_overridden_error/radio-mandatory.page');

    beforeEach(function() {
      openQuestionnaire('test_radio_mandatory_with_mandatory_other_overridden_error.json');
    });

    it('When I submit without any data in the other text field it should Then throw an overridden error', function() {
      cy
        .get(RadioMandatoryPage.other()).click()
        .get(RadioMandatoryPage.submit()).click()
        .get(RadioMandatoryPage.errorNumber(1)).stripText().should('contain', 'Test error message is overridden');
    });
  });


  describe('Given I start a Mandatory Radio Other survey ', function() {

    var RadioMandatoryPage = require('../../../../generated_pages/radio_mandatory_with_optional_other/radio-mandatory.page');
    var RadioSummaryPage = require('../../../../generated_pages/radio_mandatory_with_optional_other/summary.page');

    beforeEach(function() {
      openQuestionnaire('test_radio_mandatory_with_optional_other.json');
    });

    it('When I submit without any data in the other text field is selected, Then the selected option should be displayed in the summary', function() {
      cy
        .get(RadioMandatoryPage.submit()).click()
        .url().should('contain', RadioSummaryPage.pageName)
        .get(RadioSummaryPage.radioMandatoryAnswer()).stripText().should('contain', 'No answer provided');
    });
  });


  describe('Given I start a Mandatory Radio Other Overridden error survey  ', function() {

    var RadioMandatoryPage = require('../../../../generated_pages/radio_mandatory_with_overridden_error/radio-mandatory.page');

    beforeEach(function() {
      openQuestionnaire('test_radio_mandatory_with_overridden_error.json');
    });

    it('When I have submitted the page without any option, Then an overridden error is displayed', function() {
      cy
        .get(RadioMandatoryPage.submit()).click()
        .get(RadioMandatoryPage.errorNumber(1)).stripText().should('contain', 'Test error message is overridden');
    });
  });

  describe('Given I start a Optional survey', function() {

    var RadioNonMandatoryPage = require('../../../../generated_pages/radio_optional/radio-non-mandatory.page');
    var RadioSummaryPage = require('../../../../generated_pages/radio_optional/summary.page');

    beforeEach(function() {
      openQuestionnaire('test_radio_optional.json');
    });

    it('When I have selected no option, Then the selected option should be displayed in the summary', function() {
      cy
       .get(RadioNonMandatoryPage.submit()).click()
       .url().should('contain', RadioSummaryPage.pageName)
       .get(RadioSummaryPage.radioNonMandatoryAnswer()).stripText().should('contain', 'No answer provided');
    });
  });

  describe('Given I start a Optional Other Overridden error survey', function() {

    var RadioNonMandatoryPage = require('../../../../generated_pages/radio_optional_with_mandatory_other_overridden_error/radio-non-mandatory.page');

    beforeEach(function() {
      openQuestionnaire('test_radio_optional_with_mandatory_other_overridden_error.json');
    });

    it('When I have submitted an other option with an empty text field, Then an overridden error is displayed', function() {
      cy
        .get(RadioNonMandatoryPage.other()).click()
        .get(RadioNonMandatoryPage.submit()).click()
        .get(RadioNonMandatoryPage.errorNumber(1)).stripText().should('contain', 'Test error message is overridden');
    });
  });


  describe('Given I Start a Optional Mandatory Other survey', function() {

    var RadioNonMandatoryPage = require('../../../../generated_pages/radio_optional_with_mandatory_other/radio-non-mandatory.page');
    var RadioSummaryPage = require('../../../../generated_pages/radio_optional_with_mandatory_other/summary.page');

    beforeEach(function() {
      openQuestionnaire('test_radio_optional_with_mandatory_other.json');
    });

    it('When I submit data in the other text field it should be persisted and Then displayed on the summary', function() {
      cy
       .get(RadioNonMandatoryPage.other()).click()
       .get(RadioNonMandatoryPage.otherDetail()).type('Hello World')
       .get(RadioNonMandatoryPage.submit()).click()
       .url().should('contain', RadioSummaryPage.pageName)
       .get(RadioSummaryPage.radioNonMandatoryAnswer()).stripText().should('contain', 'Hello World');
    });
  });
});
