const helpers = require('../../../helpers');

const CheckboxNumericDetailPage = require('../../../generated_pages/checkbox_numeric_detail_answers/checkbox-numeric-detail.page');
const SummaryPage = require('../../../generated_pages/checkbox_numeric_detail_answers/summary.page');

describe('Checkbox with a numeric "detail_answer" option', function() {

  const checkbox_schema = 'test_checkbox_numeric_detail_answers.json';

  it('Given a numeric detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
      // Then
        .isVisible(CheckboxNumericDetailPage.otherDetail()).should.eventually.be.true;
    });
  });

  it('Given a numeric detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
        .isVisible(CheckboxNumericDetailPage.otherDetail()).should.eventually.be.true
        .click(CheckboxNumericDetailPage.submit())
      // Then
        .getText(SummaryPage.checkboxNumericDetailAnswer()).should.eventually.contain('Other');
    });
  });

  it('Given a numeric detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
        .setValue(CheckboxNumericDetailPage.otherDetail(), '15')
        .click(CheckboxNumericDetailPage.submit())
      // Then
        .getText(SummaryPage.checkboxNumericDetailAnswer()).should.eventually.contain('15');
    });
  });

  it('Given a numeric detail answer, When the user provides text, An error should be displayed', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
        .setValue(CheckboxNumericDetailPage.otherDetail(), 'fhdjkshfjkds')
        .click(CheckboxNumericDetailPage.submit())
      // Then
        .isVisible(CheckboxNumericDetailPage.error()).should.eventually.be.true
        .getText(CheckboxNumericDetailPage.errorNumber(1)).should.eventually.contain('Please enter an integer');
    });
  });

  it('Given a numeric detail answer, When the user provides a number larger than 20, An error should be displayed', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
        .setValue(CheckboxNumericDetailPage.otherDetail(), '250')
        .click(CheckboxNumericDetailPage.submit())
      // Then
        .isVisible(CheckboxNumericDetailPage.error()).should.eventually.be.true
        .getText(CheckboxNumericDetailPage.errorNumber(1)).should.eventually.contain('Number is too large');
    });
  });

  it('Given a numeric detail answer, When the user provides a number less than 0, An error should be displayed', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
        .setValue(CheckboxNumericDetailPage.otherDetail(), '-1')
        .click(CheckboxNumericDetailPage.submit())
      // Then
        .isVisible(CheckboxNumericDetailPage.error()).should.eventually.be.true
        .getText(CheckboxNumericDetailPage.errorNumber(1)).should.eventually.contain('Number cannot be less than zero');
    });
  });

  it('Given a numeric detail answer, When the user provides text, An error should be displayed and the text in the textbox should be kept', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
        .setValue(CheckboxNumericDetailPage.otherDetail(), 'biscuits')
        .click(CheckboxNumericDetailPage.submit())
      // Then
        .isVisible(CheckboxNumericDetailPage.error()).should.eventually.be.true
        .getText(CheckboxNumericDetailPage.errorNumber(1)).should.eventually.contain('Please enter an integer').pause(1000)
        .getValue(CheckboxNumericDetailPage.otherDetail()).should.eventually.contain('biscuits');
    });
  });

  it('Given a numeric detail answer, When the user enters "0" and submits, Then "0" should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
        .setValue(CheckboxNumericDetailPage.otherDetail(), '0')
        .click(CheckboxNumericDetailPage.submit())
      // Then
      .getText(SummaryPage.checkboxNumericDetailAnswer()).should.eventually.contain('0');
    });
  });
});
