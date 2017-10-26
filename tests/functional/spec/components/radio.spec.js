const helpers = require('../../helpers');
const RadioMandatoryPage = require('../../pages/surveys/radio/radio-mandatory.page');
const RadioNonMandatoryPage = require('../../pages/surveys/radio/radio-non-mandatory.page');
const SummaryPage = require('../../pages/surveys/radio/radio-summary.page');

describe('Radio button with an option', function() {

var radio_schema = 'test_radio.json';

it('Given an mandatory option is available, when the user clicks the mandatory option then they should be taken to the next page', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        // Nothing should be selected by default
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.sausage()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.other()).should.eventually.be.false

        // Choose Bacon option
        .click(RadioMandatoryPage.bacon())
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.true

        // Submit answers given on mandatory page
        .click(RadioMandatoryPage.submit())

         // Skipping non-mandatory page
        .click(RadioNonMandatoryPage.submit())

        // Then my answer is shown on the summary
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Bacon');
    });
  });

it('Given an optional option is available, when the user clicks a optional value then they should be taken to the next page', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
         // Nothing should be selected by default
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.sausage()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.other()).should.eventually.be.false

        // Choose Bacon option
        .click(RadioMandatoryPage.bacon())
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.true

        // Submit answers given on mandatory page
        .click(RadioMandatoryPage.submit())

        // Nothing should be selected by default
        .isSelected(RadioNonMandatoryPage.none()).should.eventually.be.false
        .isSelected(RadioNonMandatoryPage.toast()).should.eventually.be.false
        .isSelected(RadioNonMandatoryPage.coffee()).should.eventually.be.false
        .isSelected(RadioNonMandatoryPage.tea()).should.eventually.be.false
        .isSelected(RadioNonMandatoryPage.other()).should.eventually.be.false

        // Choose Coffee option
        .click(RadioNonMandatoryPage.coffee())
        .isSelected(RadioNonMandatoryPage.coffee()).should.eventually.be.true

        // Submit answers given on non-mandatory page
        .click(RadioNonMandatoryPage.submit())

        // Then my answers are shown on the summary page
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Bacon')
        .getText(SummaryPage.answer_optional()).should.eventually.contain('Coffee');
    });
  });

it('Given options are available, when values are entered these answers are displayed on the summary page', function() {
  return helpers.openQuestionnaire(radio_schema).then(() => {
    return browser
     // None should not be selected by default
     .isSelected(RadioMandatoryPage.none()).should.eventually.be.false

     // Choose none option
     .click(RadioMandatoryPage.none())
     .isSelected(RadioMandatoryPage.none()).should.eventually.be.true

     // Submit answers given on mandatory page
     .click(RadioMandatoryPage.submit())

     // None option should not be selected by default
     .isSelected(RadioNonMandatoryPage.coffee()).should.eventually.be.false

     // Choose None option
     .click(RadioNonMandatoryPage.coffee())
     .isSelected(RadioNonMandatoryPage.coffee()).should.eventually.be.true

     // Submit answers given on non-mandatory page
     .click(RadioNonMandatoryPage.submit())

     // Then the answers are shown on the summary page
     .getUrl().should.eventually.contain(SummaryPage.pageName)
     .getText(SummaryPage.answer_mandatory()).should.eventually.contain('None')
     .getText(SummaryPage.answer_optional()).should.eventually.contain('Coffee');
    });
  });

it('Given when I update my answers the content on the summary page is updated', function() {
  return helpers.openQuestionnaire(radio_schema).then(() => {
    return browser
      // Nothing should be selected by default
      .isSelected(RadioMandatoryPage.none()).should.eventually.be.false
      .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.false
      .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.false
      .isSelected(RadioMandatoryPage.sausage()).should.eventually.be.false
      .isSelected(RadioMandatoryPage.other()).should.eventually.be.false

      // Choose Eggs first
      .click(RadioMandatoryPage.eggs())
      .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.true

      // Submit answers given on mandatory page
      .click(RadioMandatoryPage.submit())

      // Skipping non-mandatory page
      .click(RadioNonMandatoryPage.submit())

       // Then my answer is shown
      .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Eggs')

       // When I return to the previous screen
      .click(SummaryPage.previous())

      // Click non-mandatory option
      .click(RadioNonMandatoryPage.tea())
      .isSelected(RadioNonMandatoryPage.tea()).should.eventually.be.true

      // Submit answers given on non-mandatory page
      .click(RadioNonMandatoryPage.submit())

      // Then the answers are shown on the summary page and updated to include non-mandatory answer
      .getUrl().should.eventually.contain(SummaryPage.pageName)
      .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Eggs')
      .getText(SummaryPage.answer_optional()).should.eventually.contain('Tea');
    });
  });

it('Given the "other" option is available, when I clicks the "other" option then the other input should be visible', function() {
     return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        // When I click on the other option
        .click(RadioMandatoryPage.other())

        // Then the text box field should be displayed when other option has been selected
        .isVisible(RadioMandatoryPage.otherText()).should.eventually.be.true;
    });
  });

it('Given I enter a value into the other input field, when I submit the page that value should be displayed on the summary.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        // When I click on the other option and set its value
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Hello')

        // Submit answers given on mandatory page
        .click(RadioMandatoryPage.submit())

         // Skipping non-mandatory page
        .click(RadioNonMandatoryPage.submit())

        // Then the answer on the summary page should contain the value from the other option text field
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Hello');
    });
    });

it('Given an "other" text field is optional on the non mandatory page, then this value will allow me to move onto the summary.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        // When I click on the other option and set its value
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Hello')

        // Submit answers given on mandatory page
        .click(RadioMandatoryPage.submit())

        // Select other option on non-mandatory page without entering any value
        .click(RadioNonMandatoryPage.other())

         // Submit answers given on non-mandatory page
        .click(RadioNonMandatoryPage.submit())

        // Then the non-mandatory answer on the summary page should be displayed
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Hello')
        .getText(SummaryPage.answer_optional()).should.eventually.contain('No answer provided');
    });
    });

it('Given an "other" text field is optional on the non mandatory page, then I submit this value and return to remove the "other" this will be displayed on the summary page', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        // When I click on the other option and set its value
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Hello')

        // Submit answers given on mandatory page
        .click(RadioMandatoryPage.submit())

        // Click non-mandatory option
        .click(RadioNonMandatoryPage.other())
        .setValue(RadioNonMandatoryPage.otherText(), 'World')

        // Submit answers given on non-mandatory page
        .click(RadioNonMandatoryPage.submit())

        // Return to previous non-mandatory page
        .click(SummaryPage.previous())

        // Remove text in other field and submit this answer
        .click(RadioNonMandatoryPage.other())
        .setValue(RadioNonMandatoryPage.otherText(), '')
        .click(RadioNonMandatoryPage.submit())

        // Then the answers on the summary page should be displayed
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Hello')
        .getText(SummaryPage.answer_optional()).should.eventually.contain('No answer provided');
    });
    });

it('Given no option is selected on the mandatory page and error is thrown ', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        // Submit no answers given on mandatory page
        .click(RadioMandatoryPage.submit())

        // Error thrown is present on screen
        .isVisible(RadioMandatoryPage.error()).should.eventually.be.true;
    });
    });
});
