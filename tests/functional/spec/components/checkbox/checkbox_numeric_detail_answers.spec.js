const helpers = require('../../../helpers');

const CheckboxNumericDetailPage = require('../../../generated_pages/checkbox_numeric_detail_answers/checkbox-numeric-detail.page');
const SummaryPage = require('../../../generated_pages/checkbox_numeric_detail_answers/summary.page');

describe('Checkbox with a numeric "detail_answer" option', function() {
  let browser;

  beforeEach(function() {
    browser = helpers.openQuestionnaire('test_checkbox_numeric_detail_answers.json').then(openBrowser => browser = openBrowser);
    $(CheckboxNumericDetailPage.other()).click();
  });

  it('Given a numeric detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    expect($(CheckboxNumericDetailPage.otherDetail()).isDisplayed()).to.be.true;
  });

  it('Given a numeric detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
    // When
      expect($(CheckboxNumericDetailPage.otherDetail()).isDisplayed()).to.be.true;
      $(CheckboxNumericDetailPage.submit()).click();
    // Then
      expect($(SummaryPage.checkboxNumericDetailAnswer()).getText()).to.contain('Other');
  });

  it('Given a numeric detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
    // When
      $(CheckboxNumericDetailPage.otherDetail()).setValue('15');
      $(CheckboxNumericDetailPage.submit()).click();
    // Then
      expect($(SummaryPage.checkboxNumericDetailAnswer()).getText()).to.contain('15');
  });

  it('Given a numeric detail answer, When the user provides text, An error should be displayed', function() {
    // When
      $(CheckboxNumericDetailPage.otherDetail()).setValue('fhdjkshfjkds');
      $(CheckboxNumericDetailPage.submit()).click();
    // Then
      expect($(CheckboxNumericDetailPage.error()).isDisplayed()).to.be.true;
      expect($(CheckboxNumericDetailPage.errorNumber(1)).getText()).to.contain('Please enter an integer');
  });

  it('Given a numeric detail answer, When the user provides a number larger than 20, An error should be displayed', function() {
    // When
      $(CheckboxNumericDetailPage.otherDetail()).setValue('250');
      $(CheckboxNumericDetailPage.submit()).click();
    // Then
      expect($(CheckboxNumericDetailPage.error()).isDisplayed()).to.be.true;
      expect($(CheckboxNumericDetailPage.errorNumber(1)).getText()).to.contain('Number is too large');
  });

  it('Given a numeric detail answer, When the user provides a number less than 0, An error should be displayed', function() {
    // When
      $(CheckboxNumericDetailPage.otherDetail()).setValue('-1');
      $(CheckboxNumericDetailPage.submit()).click();
    // Then
      expect($(CheckboxNumericDetailPage.error()).isDisplayed()).to.be.true;
      expect($(CheckboxNumericDetailPage.errorNumber(1)).getText()).to.contain('Number cannot be less than zero');
  });

  it('Given a numeric detail answer, When the user provides text, An error should be displayed and the text in the textbox should be kept', function() {
    // When
      $(CheckboxNumericDetailPage.otherDetail()).setValue('biscuits');
      $(CheckboxNumericDetailPage.submit()).click();
    // Then
      expect($(CheckboxNumericDetailPage.error()).isDisplayed()).to.be.true;
      expect($(CheckboxNumericDetailPage.errorNumber(1)).getText()).to.contain('Please enter an integer');
      browser.pause(1000);
      $(CheckboxNumericDetailPage.otherDetail()).getValue();
  });

  it('Given a numeric detail answer, When the user enters "0" and submits, Then "0" should be displayed on the summary screen', function() {
    // When
      $(CheckboxNumericDetailPage.otherDetail()).setValue('0');
      $(CheckboxNumericDetailPage.submit()).click();
    // Then
      expect($(SummaryPage.checkboxNumericDetailAnswer()).getText()).to.contain('0');
  });
});
