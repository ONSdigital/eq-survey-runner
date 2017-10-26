const helpers = require('../../helpers');
const RadioMandatoryPage = require('../../pages/surveys/radio/radio-mandatory.page');
const RadioNonMandatoryPage = require('../../pages/surveys/radio/radio-non-mandatory.page');
const SummaryPage = require('../../pages/surveys/radio/radio-summary.page');

describe('Radio button with an option', function() {

var radio_schema = 'test_radio.json';

it('Given an MANDATORY option is available, when the user clicks the MANDATORY option then they should be taken to the next page', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        // Nothing should be selected by default
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.sausage()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.other()).should.eventually.be.false

        // choose Bacon option
        .click(RadioMandatoryPage.bacon())
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.true

        // When I go to the summary
        .click(RadioMandatoryPage.submit())

         // skipping non-mandatory page
        .click(RadioNonMandatoryPage.submit())

        // Then my answer is shown
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Bacon');
    });
  });


it('Given an OPTIONAL option is available, when the user clicks a OPTIONAL value then they should be taken to the next page', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
         // Nothing should be selected by default
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.sausage()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.other()).should.eventually.be.false

        // choose Bacon option
        .click(RadioMandatoryPage.bacon())
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.true

        // When I summit that page
        .click(RadioMandatoryPage.submit())

        // Nothing should be selected by default
        .isSelected(RadioNonMandatoryPage.none()).should.eventually.be.false
        .isSelected(RadioNonMandatoryPage.toast()).should.eventually.be.false
        .isSelected(RadioNonMandatoryPage.coffee()).should.eventually.be.false
        .isSelected(RadioNonMandatoryPage.tea()).should.eventually.be.false
        .isSelected(RadioNonMandatoryPage.other()).should.eventually.be.false

        // choose Coffee option
        .click(RadioNonMandatoryPage.coffee())
        .isSelected(RadioNonMandatoryPage.coffee()).should.eventually.be.true

        // When I go to the summary
        .click(RadioNonMandatoryPage.submit())

        // Then my answer is shown
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

     // choose none option
     .click(RadioMandatoryPage.none())
     .isSelected(RadioMandatoryPage.none()).should.eventually.be.true

     // When I submit that page
     .click(RadioMandatoryPage.submit())

     // None option should be selected by default
     .isSelected(RadioNonMandatoryPage.coffee()).should.eventually.be.false

     // choose None option
     .click(RadioNonMandatoryPage.coffee())
     .isSelected(RadioNonMandatoryPage.coffee()).should.eventually.be.true

     // When I go to the summary
     .click(RadioNonMandatoryPage.submit())

     // Then the answers selected are displayed on the summary screen content
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

      // choose Eggs first
      .click(RadioMandatoryPage.eggs())
      .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.true
      .click(RadioMandatoryPage.submit())

      // skipping non-mandatory page
      .click(RadioNonMandatoryPage.submit())

       // Then my answer is shown
      .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Eggs')

       // When I return to the screen
      .click(SummaryPage.previous())

      // click non mandatory
      .click(RadioNonMandatoryPage.tea())
      .isSelected(RadioNonMandatoryPage.tea()).should.eventually.be.true

      // When I go to the summary
      .click(RadioNonMandatoryPage.submit())

      // Then the answers selected are displayed on the summary screen content
      .getUrl().should.eventually.contain(SummaryPage.pageName)
      .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Eggs')
      .getText(SummaryPage.answer_optional()).should.eventually.contain('Tea');
    });
  });


it('Given the "other" option is available, when I clicks the "other" option then the other input should be visible', function() {
     return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .getText(RadioMandatoryPage.otherLabel()).should.eventually.contain('An answer is required.')
        .click(RadioMandatoryPage.other())
        .isVisible(RadioMandatoryPage.otherText()).should.eventually.be.true;
    });
  });


it('Given I enter a value into the other input field, when I submit the page that value should be displayed on the summary.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Hello')
        .click(RadioMandatoryPage.submit())
        .click(RadioNonMandatoryPage.submit())
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Hello');
    });
    });


it('Given an "other" text field is optional on the non mandatory page, then this value will allow me to move onto the summary.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Hello')
        .click(RadioMandatoryPage.submit())
        .click(RadioNonMandatoryPage.other())
        .click(RadioNonMandatoryPage.submit())
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Hello')
        .getText(SummaryPage.answer_optional()).should.eventually.contain('No answer provided');
    });
    });


it('Given an "other" text field is optional on the non mandatory page, then I submit this value and return to remove the "other" this will be displayed on the summary page', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Hello')
        .click(RadioMandatoryPage.submit())
        .click(RadioNonMandatoryPage.other())
        .click(RadioNonMandatoryPage.submit())
        .getText(SummaryPage.answer_mandatory()).should.eventually.contain('Hello')
        .getText(SummaryPage.answer_optional()).should.eventually.contain('No answer provided');
    });
    });


it('Given no option is selected on the mandatory page and error is thrown ', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(RadioMandatoryPage.submit())
        .isVisible(RadioMandatoryPage.error()).should.eventually.be.true;
    });
    });
});
