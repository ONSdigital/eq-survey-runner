import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import MandatoryRadioPage from '../pages/surveys/radio/mandatory-radio.page'
import OptionalRadioPage from '../pages/surveys/radio/optional-radio.page'
import SummaryPage from '../pages/surveys/radio/summary.page'

const expect = chai.expect

describe('Radio button with "other" option', function() {

  var radio_schema = 'test_radio.json';

  it('Given an "other" option is available, when the user clicks the "other" option then other input should be visible', function() {
    //Given
    startQuestionnaire(radio_schema)

    //When
    MandatoryRadioPage.clickOther()

    // Then
    expect(MandatoryRadioPage.otherInputFieldExists()).to.be.true
  })

  it('Given I enter a value into the other input field, when I submit the page, then value should be displayed on the summary.', function() {
    //Given
    startQuestionnaire(radio_schema)

    // When
    MandatoryRadioPage.clickOther().setOtherInputField('Hello').submit()
    OptionalRadioPage.submit(); // Skip second page.


    //Then
    expect(SummaryPage.getPage1Answer()).to.contain('Hello')
  })

  it('Given a mandatory radio answer, when I select "Other" and submit without completing the other input field, then an error must be displayed.', function() {
    //Given
    startQuestionnaire(radio_schema)

    //When
    MandatoryRadioPage.clickOther().submit();

    //Then
    expect(MandatoryRadioPage.errorExists()).to.be.true
  })

  it('Given a mandatory radio answer and error is displayed for other input field, when I enter value and submit page, then the error should be cleared.', function() {
    //Given
    startQuestionnaire(radio_schema);

    //When
    MandatoryRadioPage.clickOther().submit();
    expect(MandatoryRadioPage.errorExists()).to.be.true
    MandatoryRadioPage.clickOther().setOtherInputField('Other Text').submit()

    //Then
    expect(OptionalRadioPage.errorExists()).to.be.false
  })

  it('Given I have previously added text in other texfiled and saved, when I change the awnser to a diffrent answer, then the text entered in other field must be wiped.', function() {
    //Given
    startQuestionnaire(radio_schema);

    //When
    MandatoryRadioPage.clickOther().setOtherInputField('Other Text').submit()
    OptionalRadioPage.clickTopprevious()
    MandatoryRadioPage.clickBacon().submit()
    OptionalRadioPage.clickTopprevious()

    //Then
    MandatoryRadioPage.clickOther()
    expect(MandatoryRadioPage.getOtherInputField()).to.equal('')
  })

})
