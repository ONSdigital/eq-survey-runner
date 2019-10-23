const helpers = require('../../../helpers');

const RadioNumericDetailPage = require('../../../generated_pages/radio_numeric_detail_answers/radio-numeric-detail.page');
const SummaryPage = require('../../../generated_pages/radio_numeric_detail_answers/summary.page');

describe('Radio with a numeric "detail_answer" option', function() {
  beforeEach(function() {
    helpers.openQuestionnaire('test_radio_numeric_detail_answers.json');
    $(RadioNumericDetailPage.other()).click();
  });

  it('Given a numeric detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    expect($(RadioNumericDetailPage.otherDetail()).isDisplayed()).to.be.true;
  });

  it('Given a numeric detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
      // When
        expect($(RadioNumericDetailPage.otherDetail()).isDisplayed()).to.be.true;
        $(RadioNumericDetailPage.submit()).click();
      // Then
        expect($(SummaryPage.radioAnswerNumericDetail()).getText()).to.contain('Other');
  });

  it('Given a numeric detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
      // When
        $(RadioNumericDetailPage.otherDetail()).setValue('15');
        $(RadioNumericDetailPage.submit()).click();
      // Then
        expect($(SummaryPage.radioAnswerNumericDetail()).getText()).to.contain('15');
  });

  it('Given a numeric detail answer, When the user provides text, An error should be displayed', function() {
      // When
        $(RadioNumericDetailPage.otherDetail()).setValue('fhdjkshfjkds');
        $(RadioNumericDetailPage.submit()).click();
      // Then
        expect($(RadioNumericDetailPage.error()).isDisplayed()).to.be.true;
        expect($(RadioNumericDetailPage.errorNumber(1)).getText()).to.contain('Please enter an integer');
  });

  it('Given a numeric detail answer, When the user provides a number larger than 20, An error should be displayed', function() {
      // When
        $(RadioNumericDetailPage.otherDetail()).setValue('250');
        $(RadioNumericDetailPage.submit()).click();
      // Then
        expect($(RadioNumericDetailPage.error()).isDisplayed()).to.be.true;
        expect($(RadioNumericDetailPage.errorNumber(1)).getText()).to.contain('Number is too large');
  });

  it('Given a numeric detail answer, When the user provides a number less than 0, An error should be displayed', function() {
      // When
        $(RadioNumericDetailPage.otherDetail()).setValue('-1');
        $(RadioNumericDetailPage.submit()).click();
      // Then
        expect($(RadioNumericDetailPage.error()).isDisplayed()).to.be.true;
        expect($(RadioNumericDetailPage.errorNumber(1)).getText()).to.contain('Number cannot be less than zero');
  });

  it('Given a numeric detail answer, When the user provides text, An error should be displayed and the text in the textbox should be kept', function() {
      // When
        $(RadioNumericDetailPage.otherDetail()).setValue('biscuits');
        $(RadioNumericDetailPage.submit()).click();
      // Then
        expect($(RadioNumericDetailPage.error()).isDisplayed()).to.be.true;
        expect($(RadioNumericDetailPage.errorNumber(1)).getText()).to.contain('Please enter an integer');
        expect($(RadioNumericDetailPage.otherDetail()).getValue()).to.contain('biscuits');
  });

  it('Given a numeric detail answer, When the user enters "0" and submits, Then "0" should be displayed on the summary screen', function() {
      // When
        $(RadioNumericDetailPage.otherDetail()).setValue('0');
        $(RadioNumericDetailPage.submit()).click();
      // Then
        expect($(SummaryPage.radioAnswerNumericDetail()).getText()).to.contain('0');
  });
});
