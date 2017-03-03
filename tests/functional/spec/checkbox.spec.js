import {openQuestionnaire} from '../helpers'

import MandatoryCheckboxPage from '../pages/surveys/checkbox/mandatory-checkbox.page'
import NonMandatoryCheckboxPage from '../pages/surveys/checkbox/non-mandatory-checkbox.page'
import SummaryPage from '../pages/surveys/checkbox/summary.page'


describe('Checkbox with "other" option', function() {

  var checkbox_schema = 'test_checkbox.json';

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible.', function() {
    openQuestionnaire(checkbox_schema)

    MandatoryCheckboxPage.clickOther();

    expect(MandatoryCheckboxPage.isOtherInputFieldVisible()).to.be.true
  })

  it('Given a mandatory checkbox answer, When I select the other option, leave the input field empty and submit, Then an error should be displayed.', function() {
    // Given
    openQuestionnaire(checkbox_schema)

    // When
    MandatoryCheckboxPage.clickOther()
    MandatoryCheckboxPage.submit()

    // Then
    expect(MandatoryCheckboxPage.errorExists()).to.be.true
  })

  it('Given a mandatory checkbox answer, when there is an error on the page for other field and I enter valid value and submit page, then the error is cleared and I navigate to next page.s', function() {
    // Given
    openQuestionnaire(checkbox_schema)
    MandatoryCheckboxPage.clickOther().submit()
    expect(MandatoryCheckboxPage.errorExists()).to.be.true

    // When
    MandatoryCheckboxPage.setOtherInputField('Other Text').submit()

    // Then
    expect(NonMandatoryCheckboxPage.errorExists()).to.be.false
  })


  it('Given a non-mandatory checkbox answer, when the user does not select an option, then "No answer provided" should be displayed on the summary screen', function() {
     // Given
     openQuestionnaire(checkbox_schema)

     // When
     MandatoryCheckboxPage.clickOther().setOtherInputField('Other value').submit();
     NonMandatoryCheckboxPage.submit();

     // Then
     expect(SummaryPage.getNonMandatoryAnswer()).to.equal('No answer provided')

  })

  it('Given a non-mandatory checkbox answer, when the user selects Other but does not supply a value, then "Other" should be displayed on the summary screen', function() {
     // Given
     openQuestionnaire(checkbox_schema)

     // When
     MandatoryCheckboxPage.clickOther().setOtherInputField('Other value').submit();
     NonMandatoryCheckboxPage.clickOther().submit();

     // Then
     expect(SummaryPage.getNonMandatoryAnswer()).to.have.string('Other');
  })

  it('Given a non-mandatory checkbox answer, when the user selects Other and supplies a value, then the supplied value should be displayed on the summary screen', function() {
     // Given
     openQuestionnaire(checkbox_schema)

     // When
     MandatoryCheckboxPage.clickOther().setOtherInputField('Other value').submit();
     NonMandatoryCheckboxPage.clickOther().setOtherInputField('The other value').submit();

     // Then
     expect(SummaryPage.getNonMandatoryOtherAnswer()).to.have.string('The other value');
  })

  it('Given I have previously added text in other texfiled and saved, when I uncheck other options and select a different checkbox as answer, then the text entered in other field must be wiped.', function() {
     // Given
     openQuestionnaire(checkbox_schema)

     // When
     MandatoryCheckboxPage.clickOther().setOtherInputField('Other value').submit();
     NonMandatoryCheckboxPage.clickTopPrevious()
     MandatoryCheckboxPage.clickOther()
       .clickMandatoryCheckboxAnswerCheese()
       .submit()
     NonMandatoryCheckboxPage.clickTopPrevious()
     // Then
     MandatoryCheckboxPage.clickOther()
     expect(MandatoryCheckboxPage.getOtherInputField()).to.equal('')
  })

})
