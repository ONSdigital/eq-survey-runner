const helpers = require('../../../helpers');

const CheckboxNumericDetailPage = require('../../../generated_pages/checkbox_numeric_detail_answers/checkbox-numeric-detail.page');
const SummaryPage = require('../../../generated_pages/checkbox_numeric_detail_answers/summary.page');

describe('Checkbox with a numeric "detail_answer" option', function() {

  const checkbox_schema = 'test_checkbox_numeric_detail_answers.json';

  it('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
      // Then
        .isVisible(CheckboxNumericDetailPage.otherDetail()).should.eventually.be.true;
    });
  });

  it('Given a detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
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

  it('Given a detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(CheckboxNumericDetailPage.other())
        .setValue(CheckboxNumericDetailPage.otherDetail(), '1234')
        .click(CheckboxNumericDetailPage.submit())
      // Then
        .getText(SummaryPage.checkboxNumericDetailAnswer()).should.eventually.contain('1234');
    });
  });
});
