const helpers = require('../../../helpers');

const MandatoryCheckboxPage = require('../../../generated_pages/checkbox_multiple_detail_answers/mandatory-checkbox.page');
const SummaryPage = require('../../../generated_pages/checkbox_multiple_detail_answers/summary.page');

describe('Checkbox with multiple "detail_answer" options', function() {

  const checkbox_schema = 'test_checkbox_multiple_detail_answers.json';

  it('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
        .click(MandatoryCheckboxPage.yourChoice())
        .isVisible(MandatoryCheckboxPage.yourChoiceDetail()).should.eventually.be.true
        .click(MandatoryCheckboxPage.cheese())
        .isVisible(MandatoryCheckboxPage.cheeseDetail()).should.eventually.be.true;
    });
  });

  it('Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        // Non-Mandatory detail answer given
        .click(MandatoryCheckboxPage.cheese())
        .setValue(MandatoryCheckboxPage.cheeseDetail(), 'Mozzarella')
        // Mandatory detail answer left blank
        .click(MandatoryCheckboxPage.yourChoice())
        .click(MandatoryCheckboxPage.submit())
      // Then
        .isVisible(MandatoryCheckboxPage.error()).should.eventually.be.true
        .getText(MandatoryCheckboxPage.errorNumber(1)).should.eventually.contain('Enter your topping choice to continue');
    });
  });

  it('Given a selected checkbox answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
        .click(MandatoryCheckboxPage.yourChoice())
        .click(MandatoryCheckboxPage.submit())
        .isVisible(MandatoryCheckboxPage.error()).should.eventually.be.true

      // When
        .setValue(MandatoryCheckboxPage.yourChoiceDetail(), 'Bacon')
        .click(MandatoryCheckboxPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });


  it('Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.cheese())
        .isVisible(MandatoryCheckboxPage.cheeseDetail()).should.eventually.be.true
        .click(MandatoryCheckboxPage.submit())
      // Then
        .getText(SummaryPage.mandatoryCheckboxAnswer()).should.eventually.equal('Cheese');
    });
  });

  it('Given multiple detail answers, When the user provides text for all, Then that text should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.cheese())
        .setValue(MandatoryCheckboxPage.cheeseDetail(), 'Mozzarella')
        .click(MandatoryCheckboxPage.yourChoice())
        .setValue(MandatoryCheckboxPage.yourChoiceDetail(), 'Bacon')
        .click(MandatoryCheckboxPage.submit())
      // Then
        .getText(SummaryPage.mandatoryCheckboxAnswer()).should.eventually.equal('Cheese\nMozzarella\nYour choice\nBacon');
    });
  });

  it('Given multiple detail answers, When the user provides text for just one, Then that text should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.yourChoice())
        .setValue(MandatoryCheckboxPage.yourChoiceDetail(), 'Bacon')
        .click(MandatoryCheckboxPage.submit())
      // Then
        .getText(SummaryPage.mandatoryCheckboxAnswer()).should.eventually.equal('Your choice\nBacon');
    });
  });

  it('Given I have previously added text in a detail answer and saved, When I uncheck the detail answer option and select a different checkbox, Then the text entered in the detail answer field should be empty.', function() {
    // Given
    return helpers.openQuestionnaire(checkbox_schema).then(() => {
      return browser
      // When
        .click(MandatoryCheckboxPage.cheese())
        .setValue(MandatoryCheckboxPage.cheeseDetail(), 'Mozzarella')
        .click(MandatoryCheckboxPage.submit())
        .click(SummaryPage.previous())
        .click(MandatoryCheckboxPage.cheese())
        .click(MandatoryCheckboxPage.ham())
        .click(MandatoryCheckboxPage.submit())
        .click(SummaryPage.previous())
      // Then
        .click(MandatoryCheckboxPage.cheese())
        .getValue(MandatoryCheckboxPage.cheeseDetail()).should.eventually.be.equal('');
    });

  });

});
