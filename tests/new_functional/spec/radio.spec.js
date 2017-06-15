const helpers = require('../helpers');
const RadioMandatoryPage = require('../pages/surveys/radio/radio-mandatory.page');
const RadioNonMandatoryPage = require('../pages/surveys/radio/radio-non-mandatory.page');
const SummaryPage = require('../pages/surveys/radio/radio-summary.page');

describe('Radio button with "other" option', function() {

  var radio_schema = 'test_radio.json';

  it('Given an "other" option is available, when the user clicks the "other" option then other input should be visible', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(RadioMandatoryPage.other())
        .isVisible(RadioMandatoryPage.otherText()).should.eventually.be.true;
    });
  });

  it('Given I enter a value into the other input field, when I submit the page, then value should be displayed on the summary.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Hello')
        .click(RadioMandatoryPage.submit())
        .click(RadioNonMandatoryPage.submit())
        .getText(SummaryPage.answer()).should.eventually.contain('Hello');
    });

  });

  it('Given a mandatory radio answer, when I select "Other" and submit without completing the other input field, then an error must be displayed.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(RadioMandatoryPage.other())
        .click(RadioMandatoryPage.submit())
        .isVisible(RadioMandatoryPage.error()).should.eventually.be.true;
    });

  });

  it('Given a mandatory radio answer and error is displayed for other input field, when I enter value and submit page, then the error should be cleared.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // Given
        .click(RadioMandatoryPage.other())
        .click(RadioMandatoryPage.submit())
        .isVisible(RadioMandatoryPage.error()).should.eventually.be.true
      // When
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Other Text')
        .click(RadioMandatoryPage.submit())
      // Then
        .getUrl().should.eventually.contain(RadioNonMandatoryPage.pageName);
    });

  });

  it('Given I have previously added text in other textfield and saved, when I change the answer to a different answer, then the text entered in other field must be wiped.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(RadioMandatoryPage.other())
        .setValue(RadioMandatoryPage.otherText(), 'Other Text')
        .click(RadioMandatoryPage.submit())
        .click(RadioNonMandatoryPage.previous())
        .click(RadioMandatoryPage.bacon())
        .click(RadioMandatoryPage.submit())
        .click(RadioNonMandatoryPage.previous())
        .click(RadioMandatoryPage.other())
        .getValue(RadioMandatoryPage.otherText()).should.eventually.equal('');
    });

  });

  it('Given I have previously selected the None option and saved, When I return to the screen, Then my choice is remembered.', function() {
    // https://github.com/ONSdigital/eq-survey-runner/issues/1013

    return helpers.openQuestionnaire(radio_schema).then(() => {
      // Given
      return browser
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.false
      // When
        .click(RadioMandatoryPage.none())
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.true
      // Then
        .click(RadioMandatoryPage.submit())
        .click(RadioNonMandatoryPage.previous())
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.true;
    });

  });

  it('Given I have previously selected an option and saved, When I return to the screen and change my answer twice, Then my new choice is remembered and is shown on the Summary screen.', function() {
    // Given
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

      // When I return to the screen
        .click(RadioNonMandatoryPage.previous())

      // Then my choice is remembered (Eggs)
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.true
        .isSelected(RadioMandatoryPage.sausage()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.other()).should.eventually.be.false

      // When I change my answer to the None option
        .click(RadioMandatoryPage.none())
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.true
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.sausage()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.other()).should.eventually.be.false
        .click(RadioMandatoryPage.submit())

      // Then my choice is remembered when I return
        .click(RadioNonMandatoryPage.previous())
        .isSelected(RadioMandatoryPage.none()).should.eventually.be.true
        .isSelected(RadioMandatoryPage.bacon()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.eggs()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.sausage()).should.eventually.be.false
        .isSelected(RadioMandatoryPage.other()).should.eventually.be.false

      // When I change my answer for the last time to Sausage
        .click(RadioMandatoryPage.sausage())

      // When I go to the summary
        .click(RadioMandatoryPage.submit())

      // skipping non-mandatory page
        .click(RadioNonMandatoryPage.submit())

      // Then my answer is shown
        .getText(SummaryPage.answer()).should.eventually.contain('Sausage');
    });
  });
});
