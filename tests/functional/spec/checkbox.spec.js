import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import MandatoryCheckboxPage from '../pages/surveys/checkbox/mandatory-checkbox.page'
import OptionalCheckboxPage from '../pages/surveys/checkbox/optional-checkbox.page'
import SummaryPage from '../pages/surveys/checkbox/summary.page'

const expect = chai.expect

describe('Checkbox with "other" option', function() {

  var checkbox_schema = 'test_checkbox.json';

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible.', function() {
    startQuestionnaire(checkbox_schema)

    MandatoryCheckboxPage.clickOther();

    expect(MandatoryCheckboxPage.isOtherInputFieldVisible()).to.be.true
  })

  it('Given a mandatory checkbox answer, When I select the other option, leave the input field empty and submit, Then an error should be displayed.', function() {
    // Given
    startQuestionnaire(checkbox_schema)

    // When
    MandatoryCheckboxPage.clickOther()
    MandatoryCheckboxPage.submit()

    // Then
    expect(MandatoryCheckboxPage.errorExists()).to.be.true
  })

  it('Given a mandatory checkbox answer, when there is an error on the page for other field and I enter valid value and submit page, then the error is cleared and I navigate to next page.s', function() {
    // Given
    startQuestionnaire(checkbox_schema)
    MandatoryCheckboxPage.clickOther().submit()
    expect(MandatoryCheckboxPage.errorExists()).to.be.true

    // When
    MandatoryCheckboxPage.setOtherInputField('Other Text').submit()

    // Then
    expect(OptionalCheckboxPage.errorExists()).to.be.false
  })


  it('Given a non-mandatory checkbox answer, when the user does not select an option, then "No answer provided" should be displayed on the summary screen', function() {
     // Given
     startQuestionnaire(checkbox_schema)

     // When
     MandatoryCheckboxPage.clickOther().setOtherInputField('Other value').submit();
     OptionalCheckboxPage.submit();

     // Then
     expect(SummaryPage.getPage2Answer()).to.equal('No answer provided')

  })

  it('Given a non-mandatory checkbox answer, when the user selects Other but does not supply a value, then "Other" should be displayed on the summary screen', function() {
     // Given
     startQuestionnaire(checkbox_schema)

     // When
     MandatoryCheckboxPage.clickOther().setOtherInputField('Other value').submit();
     OptionalCheckboxPage.clickOther().submit();

     // Then
     expect(SummaryPage.getPage2Answer()).to.have.string('Other');
  })

  it('Given a non-mandatory checkbox answer, when the user selects Other and supplies a value, then the supplied value should be displayed on the summary screen', function() {
     // Given
     startQuestionnaire(checkbox_schema)

     // When
     MandatoryCheckboxPage.clickOther().setOtherInputField('Other value').submit();
     OptionalCheckboxPage.clickOther().setOtherInputField('The other value').submit();

     // Then
     expect(SummaryPage.getPage2OtherAnswer()).to.have.string('The other value');
  })

  it('Given I have previously added text in other texfiled and saved, when I uncheck other options and select a different checkbox as answer, then the text entered in other field must be wiped.', function() {
     // Given
     startQuestionnaire(checkbox_schema)

     // When
     MandatoryCheckboxPage.clickOther().setOtherInputField('Other value').submit();
     OptionalCheckboxPage.clickTopprevious()
     MandatoryCheckboxPage.clickOther()
     .clickCheese()
     .submit()
     OptionalCheckboxPage.clickTopprevious()
     // Then
     MandatoryCheckboxPage.clickOther()
     expect(MandatoryCheckboxPage.getOtherInputField()).to.equal('')
  })

})
