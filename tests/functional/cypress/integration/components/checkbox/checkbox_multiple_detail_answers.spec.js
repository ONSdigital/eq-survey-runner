import {openQuestionnaire} from '../../../helpers/helpers.js'

const MandatoryCheckboxPage = require('../../../../generated_pages/checkbox_multiple_detail_answers/mandatory-checkbox.page');
const SummaryPage = require('../../../../generated_pages/checkbox_multiple_detail_answers/summary.page');

describe('Checkbox with multiple "detail_answer" options', function() {

  const checkbox_schema = 'test_checkbox_multiple_detail_answers.json';

  it('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    openQuestionnaire(checkbox_schema)
      .get(MandatoryCheckboxPage.yourChoice()).click()
      .get(MandatoryCheckboxPage.yourChoiceDetail()).should('be.visible')
      .get(MandatoryCheckboxPage.cheese()).click()
      .get(MandatoryCheckboxPage.cheeseDetail()).should('be.visible');
  });

  it('Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.', function() {
    // Given
    openQuestionnaire(checkbox_schema)
      // When
      // Non-Mandatory detail answer given
      .get(MandatoryCheckboxPage.cheese()).click()
      .get(MandatoryCheckboxPage.cheeseDetail()).type('Mozzarella')
      // Mandatory detail answer left blank
      .get(MandatoryCheckboxPage.yourChoice()).click()
      .get(MandatoryCheckboxPage.submit()).click()
      // Then
      .get(MandatoryCheckboxPage.error()).should('be.visible')
      .get(MandatoryCheckboxPage.errorNumber(1)).stripText().should('contain', 'Enter your topping choice to continue');
  });

  it('Given a selected checkbox answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.', function() {
    // Given
    openQuestionnaire(checkbox_schema)
      .get(MandatoryCheckboxPage.yourChoice()).click()
      .get(MandatoryCheckboxPage.submit()).click()
      .get(MandatoryCheckboxPage.error()).should('be.visible')

      // When
      .get(MandatoryCheckboxPage.yourChoiceDetail()).type('Bacon')
      .get(MandatoryCheckboxPage.submit()).click()
      .url().should('contain', SummaryPage.pageName);
  });


  it('Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
    // Given
    openQuestionnaire(checkbox_schema)
      // When
      .get(MandatoryCheckboxPage.cheese()).click()
      .get(MandatoryCheckboxPage.cheeseDetail()).should('be.visible')
      .get(MandatoryCheckboxPage.submit()).click()
      // Then
      .get(SummaryPage.mandatoryCheckboxAnswer()).stripText().should('equal', 'Cheese');
  });

  it('Given multiple detail answers, When the user provides text for all, Then that text should be displayed on the summary screen', function() {
    // Given
    openQuestionnaire(checkbox_schema)
      // When
      .get(MandatoryCheckboxPage.cheese()).click()
      .get(MandatoryCheckboxPage.cheeseDetail()).type('Mozzarella')
      .get(MandatoryCheckboxPage.yourChoice()).click()
      .get(MandatoryCheckboxPage.yourChoiceDetail()).type('Bacon')
      .get(MandatoryCheckboxPage.submit()).click()
      // Then
      .get(SummaryPage.mandatoryCheckboxAnswer()).stripText().should('match', /Cheese\s*Mozzarella\s*Your choice\s*Bacon/);
  });

  it('Given multiple detail answers, When the user provides text for just one, Then that text should be displayed on the summary screen', function() {
    // Given
    openQuestionnaire(checkbox_schema)
      // When
      .get(MandatoryCheckboxPage.yourChoice()).click()
      .get(MandatoryCheckboxPage.yourChoiceDetail()).type('Bacon')
      .get(MandatoryCheckboxPage.submit()).click()
      // Then
      .get(SummaryPage.mandatoryCheckboxAnswer()).stripText().should('match', /Your choice\s*Bacon/);
  });

  it('Given I have previously added text in a detail answer and saved, When I uncheck the detail answer option and select a different checkbox, Then the text entered in the detail answer field should be empty.', function() {
    // Given
    openQuestionnaire(checkbox_schema)
      // When
      .get(MandatoryCheckboxPage.cheese()).click()
      .get(MandatoryCheckboxPage.cheeseDetail()).type('Mozzarella')
      .get(MandatoryCheckboxPage.submit()).click()
      .get(SummaryPage.previous()).click()
      .get(MandatoryCheckboxPage.cheese()).click()
      .get(MandatoryCheckboxPage.ham()).click()
      .get(MandatoryCheckboxPage.submit()).click()
      .get(SummaryPage.previous()).click()
      // Then
      .get(MandatoryCheckboxPage.cheese()).click()
      .get(MandatoryCheckboxPage.cheeseDetail()).should('have.value', '');
  });

});
