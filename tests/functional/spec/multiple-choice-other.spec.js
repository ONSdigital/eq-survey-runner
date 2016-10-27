import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import OtherOptionsPage from '../pages/surveys/other_option/other-options.page'
import OtherOptionsRadioPage from '../pages/surveys/other_option/other-options-radio.page'
import OtherOptionsSummary from '../pages/surveys/other_option/other-option-summary.page'
import SummaryPage from '../pages/surveys/question.page'

import PizzaToppingsPage from '../pages/surveys/checkbox_other/0/pizza-toppings.page'
import PizzaBasesPage from '../pages/surveys/checkbox_other/0/pizza-bases.page'
import CheckboxOtherSummaryPage from '../pages/surveys/checkbox_other/0/checkbox-other-summary.page'

const expect = chai.expect

describe('Multiple choice Checkbox/Radio "other" option', function() {

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible', function() {
    startQuestionnaire('0_checkbox_other.json')
    browser.click('[data-qa="has-other-option"]')
    expect(browser.isVisible('[data-qa="other-option"]')).to.be.true
  })

  it('Given a non-mandatory checkbox answer, when the user does not select an option, "No answer provided" should be displayed on the summary screen', function() {

     // Given
     startQuestionnaire('0_checkbox_other.json')

     // When
     PizzaToppingsPage.submit();
     PizzaBasesPage.selectPizzaBase('thin').submit();

     // Then
     expect(CheckboxOtherSummaryPage.getPizzaToppingAnswer()).to.equal('No answer provided')

  })

  it('Given a non-mandatory checkbox answer, when the user selects Other but does not supply a value, "Other" should be displayed on the summary screen', function() {

     // Given
     startQuestionnaire('0_checkbox_other.json')

     // When
     PizzaToppingsPage.selectOther().submit();

     PizzaBasesPage.selectPizzaBase('deep pan').submit();

     // Then
     expect(CheckboxOtherSummaryPage.getPizzaToppingAnswer()).to.have.string('Other');

  })

  it('Given a non-mandatory checkbox answer, when the user selects Other and supplies a value, the supplied value should be displayed on the summary screen', function() {

     // Given
     startQuestionnaire('0_checkbox_other.json')

     // When
     PizzaToppingsPage.selectOther().setOtherValue('The other value').submit();

     PizzaBasesPage.selectPizzaBase('deep pan').submit();

     // Then
     expect(CheckboxOtherSummaryPage.getPizzaToppingAnswer()).to.have.string('The other value');

  })

  it('Given an "other" option is available, when the user clicks the "other" option then other input should be visible', function() {

    //Given
    startQuestionnaire('0_checkbox_other.json')
    //When
    OtherOptionsPage.clickOther()

    // Then
    expect(OtherOptionsPage.otherTextFieldExits()).to.be.true
  })

  it('Given a mandatory checkbox answer, when I select the other option without entering text into the other field and submit, then an error must be displayed  ', function() {

    //Given
    startQuestionnaire('0_checkbox_other_mandatory.json')
    OtherOptionsPage.clickOther()

    //When
    OtherOptionsPage.submit()

    //Then
    expect(OtherOptionsPage.errorExists()).to.be.true
  })

  it('Given a mandatory checkbox answer, When there is an error on the page for other field and I enter valid value and submit page, Then the error is cleared and move to summary page  ', function() {

    //Given
    startQuestionnaire('0_checkbox_other_mandatory.json')
    OtherOptionsPage.clickOther()
      .submit()
    expect(OtherOptionsPage.errorExists()).to.be.true

    //When
    OtherOptionsPage.setTextInOtherField('Other Text')
      .submit()

    //Then
    expect(OtherOptionsPage.errorExists()).to.be.false

  })

  it('Given I have chosen other radio Option and entered hello in the other field When I submit page then on the summary screen I can see the text I entered displayed.  ', function() {

    //Given
    startQuestionnaire('0_radio_other.json')
    OtherOptionsPage.clickOther()
    expect(OtherOptionsPage.otherTextFieldExits()).to.be.true

    //When
    OtherOptionsPage.setTextInOtherField('Hello')
      .submit()
    OtherOptionsRadioPage.clickYes()
      .submit()

    //Then
    expect(OtherOptionsSummary.getOtherRadioSummary()).to.contain('Hello')
  })

  it('Given I have chosen other Radio Option and not entered any text in the other field and When I submit page then an error must be displayed  ', function() {

    //Given
    startQuestionnaire('0_radio_other.json')
    OtherOptionsPage.clickOther()

    //When
    OtherOptionsPage.submit()

    //Then
    expect(OtherOptionsPage.errorExists()).to.be.true

  })

  it('Given a error on the page for other radio field when I enter valid value and submit page Then error is cleared and move to summary page  ', function() {
    //Given
    startQuestionnaire('0_radio_other.json')
    OtherOptionsPage.clickOther()
      .submit()

    //When
    OtherOptionsPage.setTextInOtherField('Other Text')
      .submit()

    //Then
    expect(OtherOptionsPage.errorExists()).to.be.false

  })
})
