const helpers = require('../../../helpers');

const RadioNumericDetailPage = require('../../../generated_pages/radio_numeric_detail_answers/radio-numeric-detail.page');
const SummaryPage = require('../../../generated_pages/radio_numeric_detail_answers/summary.page');

describe('Radio with a numeric "detail_answer" option', function() {

  const radio_schema = 'test_radio_numeric_detail_answers.json';

  it('Given a numeric detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
      // Then
        .isVisible(RadioNumericDetailPage.otherDetail()).should.eventually.be.true;
    });
  });

  it('Given a numeric detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
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

  it('Given a numeric detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
        .setValue(RadioNumericDetailPage.otherDetail(), '15')
        .click(RadioNumericDetailPage.submit())
      // Then
        .getText(SummaryPage.radioAnswerNumericDetail()).should.eventually.contain('15');
    });
  });

  it('Given a numeric detail answer, When the user provides text, An error should be displayed', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
        .setValue(RadioNumericDetailPage.otherDetail(), 'fhdjkshfjkds')
        .click(RadioNumericDetailPage.submit())
      // Then
        .isVisible(RadioNumericDetailPage.error()).should.eventually.be.true
        .getText(RadioNumericDetailPage.errorNumber(1)).should.eventually.contain('Please enter an integer');
    });
  });

  it('Given a numeric detail answer, When the user provides a number larger than 20, An error should be displayed', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
        .setValue(RadioNumericDetailPage.otherDetail(), '250')
        .click(RadioNumericDetailPage.submit())
      // Then
        .isVisible(RadioNumericDetailPage.error()).should.eventually.be.true
        .getText(RadioNumericDetailPage.errorNumber(1)).should.eventually.contain('Number is too large');
    });
  });

  it('Given a numeric detail answer, When the user provides a number less than 0, An error should be displayed', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
        .setValue(RadioNumericDetailPage.otherDetail(), '-1')
        .click(RadioNumericDetailPage.submit())
      // Then
        .isVisible(RadioNumericDetailPage.error()).should.eventually.be.true
        .getText(RadioNumericDetailPage.errorNumber(1)).should.eventually.contain('Number cannot be less than zero');
    });
  });

  it('Given a numeric detail answer, When the user provides text, An error should be displayed and the text in the textbox should be kept', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
        .setValue(RadioNumericDetailPage.otherDetail(), 'biscuits')
        .click(RadioNumericDetailPage.submit())
      // Then
        .isVisible(RadioNumericDetailPage.error()).should.eventually.be.true
        .getText(RadioNumericDetailPage.errorNumber(1)).should.eventually.contain('Please enter an integer')
        .getValue(RadioNumericDetailPage.otherDetail()).should.eventually.contain('biscuits');
    });
  });

  it('Given a numeric detail answer, When the user enters "0" and submits, Then "0" should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(RadioNumericDetailPage.other())
        .setValue(RadioNumericDetailPage.otherDetail(), '0')
        .click(RadioNumericDetailPage.submit())
      // Then
        .getText(SummaryPage.radioAnswerNumericDetail()).should.eventually.contain('0');
    });
  });
});
