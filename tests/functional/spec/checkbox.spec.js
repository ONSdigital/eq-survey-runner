const helpers = require('../helpers');

const MandatoryCheckboxPage = require('../generated_pages/checkbox/mandatory-checkbox.page');
const NonMandatoryCheckboxPage = require('../generated_pages/checkbox/non-mandatory-checkbox.page');
const SummaryPage = require('../generated_pages/checkbox/summary.page');

describe('Checkbox with "other" option', function() {

  const checkbox_schema = 'test_checkbox.json';

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible.', function() {
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
        .getText(MandatoryCheckboxPage.otherLabel()).should.eventually.have.string('Choose any other topping')
        .click(MandatoryCheckboxPage.other())
        .isVisible(MandatoryCheckboxPage.otherText()).should.eventually.be.true;
    });
  });

  it('Given a mandatory checkbox answer, When I select the other option, leave the input field empty and submit, Then an error should be displayed.', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.other())
        .click(MandatoryCheckboxPage.submit())
      // Then
        .isVisible(MandatoryCheckboxPage.error()).should.eventually.be.true;
    });
  });

  it('Given a mandatory checkbox answer, when there is an error on the page for other field and I enter valid value and submit page, then the error is cleared and I navigate to next page.s', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
        .click(MandatoryCheckboxPage.other())
        .click(MandatoryCheckboxPage.submit())
        .isVisible(MandatoryCheckboxPage.error()).should.eventually.be.true

      // When
        .setValue(MandatoryCheckboxPage.otherText(), 'Other Text')
        .click(MandatoryCheckboxPage.submit())
        .getUrl().should.eventually.contain(NonMandatoryCheckboxPage.pageName);
    });
  });


  it('Given a non-mandatory checkbox answer, when the user does not select an option, then "No answer provided" should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.other())
        .setValue(MandatoryCheckboxPage.otherText(), 'Other value')
        .click(MandatoryCheckboxPage.submit())
        .click(NonMandatoryCheckboxPage.submit())
      // Then
        .getText(SummaryPage.nonMandatoryCheckboxAnswer()).should.eventually.equal('No answer provided');
    });
  });

  it('Given a non-mandatory checkbox answer, when the user selects Other but does not supply a value, then "Other" should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.other())
        .setValue(MandatoryCheckboxPage.otherText(), 'Other value')
        .click(MandatoryCheckboxPage.submit())
        .click(NonMandatoryCheckboxPage.other())
        .click(NonMandatoryCheckboxPage.submit())
      // Then
        .getText(SummaryPage.nonMandatoryCheckboxAnswer()).should.eventually.have.string('Other');
    });

  });

  it('Given a non-mandatory checkbox answer, when the user selects Other and supplies a value, then the supplied value should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.other())
        .setValue(MandatoryCheckboxPage.otherText(), 'Other value')
        .click(MandatoryCheckboxPage.submit())
        .click(NonMandatoryCheckboxPage.other())
        .setValue(NonMandatoryCheckboxPage.otherText(), 'The other value')
        .click(NonMandatoryCheckboxPage.submit())
      // Then
        .getText(SummaryPage.nonMandatoryCheckboxAnswer()).should.eventually.have.string('The other value');

    });

  });

  it('Given I have previously added text in other texfiled and saved, when I uncheck other options and select a different checkbox as answer, then the text entered in other field must be wiped.', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.other())
        .setValue(MandatoryCheckboxPage.otherText(), 'Other value')
        .click(MandatoryCheckboxPage.submit())
        .click(NonMandatoryCheckboxPage.previous())
        .click(MandatoryCheckboxPage.other())
        .click(MandatoryCheckboxPage.cheese())
        .click(MandatoryCheckboxPage.submit())
        .click(NonMandatoryCheckboxPage.previous())
      // Then
        .click(MandatoryCheckboxPage.other())
        .getValue(MandatoryCheckboxPage.otherText()).should.eventually.be.equal('');
    });

  });

  it('Given a mandatory checkbox answer, when the user selects only one option, then the answer should not be displayed as a list on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.ham())
        .click(MandatoryCheckboxPage.submit())
        .click(NonMandatoryCheckboxPage.submit())
      // Then
        .element(SummaryPage.mandatoryCheckboxAnswer()).elements('li').then(result => result.value).should.eventually.be.empty;
    });
  });

    it('Given a mandatory checkbox answer, when the user selects more than one option, then the answer should be displayed as a list on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.ham())
        .click(MandatoryCheckboxPage.cheese())
        .click(MandatoryCheckboxPage.submit())
        .click(NonMandatoryCheckboxPage.submit())
      // Then
        .element(SummaryPage.mandatoryCheckboxAnswer()).elements('li').then(result => result.value.length).should.eventually.be.equal(2);
    });
  });

});
