import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import OtherOptionsPage from '../pages/surveys/other_option/other-options.page'
import OtherOptionsRadioPage from '../pages/surveys/other_option/other-options-radio.page'
import OtherOptionsSummary from '../pages/surveys/other_option/other-option-summary.page'
import SummaryPage from '../pages/surveys/question.page'

const expect = chai.expect

describe('Multiple choice Checkbox/Radio "other" option', function() {

  it('Given an "other" option is available, when the user clicks the "other" option then other input should be visible', function() {

    //Given
    startQuestionnaire('0_checkbox_other.json')
    //When
    OtherOptionsPage.clickOther()

    // Then
    expect(OtherOptionsPage.otherTextFieldExits()).to.be.true
  })

  it('Given I have chosen other Option and not entered any text in the other field When I submit page then an error must be displayed  ', function() {

    //Given
    startQuestionnaire('0_checkbox_other.json')
    OtherOptionsPage.clickOther()

    //When
    OtherOptionsPage.submit()

    //Then
    expect(OtherOptionsPage.errorExists()).to.be.true
  })

  it('Given a error on the page for other field when I enter valid value and submit page Then error is cleared and move to summary page  ', function() {

    //Given
    startQuestionnaire('0_checkbox_other.json')
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
