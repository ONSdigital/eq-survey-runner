const helpers = require('../../../helpers');

const RadioNumericDetailPage = require('../../../generated_pages/radio_numeric_detail_answers/radio-numeric-detail.page');
const SummaryPage = require('../../../generated_pages/radio_numeric_detail_answers/summary.page');

describe('Radio with a numeric "detail_answer" option', function() {

  const radio_schema = 'test_radio_numeric_detail_answers.json';

  it('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
      // Then
        .isVisible(RadioNumericDetailPage.otherDetail()).should.eventually.be.true;
    });
  });

  it('Given a detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
        .isVisible(RadioNumericDetailPage.otherDetail()).should.eventually.be.true
        .click(RadioNumericDetailPage.submit())
      // Then
        .getText(SummaryPage.radioAnswerNumericDetail()).should.eventually.contain('Other');
    });
  });

  it('Given a detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
        .setValue(RadioNumericDetailPage.otherDetail(), '1234')
        .click(RadioNumericDetailPage.submit())
      // Then
        .getText(SummaryPage.radioAnswerNumericDetail()).should.eventually.contain('1234');
    });
  });
});
