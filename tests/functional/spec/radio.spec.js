import {openQuestionnaire} from '../helpers'
import RadioMandatoryPage from '../pages/surveys/radio/radio-mandatory.page'
import RadioNonMandatoryPage from '../pages/surveys/radio/radio-non-mandatory.page'
import SummaryPage from '../pages/surveys/radio/summary.page'


describe('Radio button with "other" option', function() {

  var radio_schema = 'test_radio.json';

  it('Given an "other" option is available, when the user clicks the "other" option then other input should be visible', function() {
    //Given
    openQuestionnaire(radio_schema)

    //When
    RadioMandatoryPage.clickOther()

    // Then
    expect(RadioMandatoryPage.otherInputFieldExists()).to.be.true
  })

  it('Given I enter a value into the other input field, when I submit the page, then value should be displayed on the summary.', function() {
    //Given
    openQuestionnaire(radio_schema)

    // When
    RadioMandatoryPage.clickOther().setOtherInputField('Hello').submit()
    RadioNonMandatoryPage.submit(); // Skip second page.


    //Then
    expect(SummaryPage.getMandatoryOtherAnswer()).to.contain('Hello')
  })

  it('Given a mandatory radio answer, when I select "Other" and submit without completing the other input field, then an error must be displayed.', function() {
    //Given
    openQuestionnaire(radio_schema)

    //When
    RadioMandatoryPage.clickOther().submit();

    //Then
    expect(RadioMandatoryPage.errorExists()).to.be.true
  })

  it('Given a mandatory radio answer and error is displayed for other input field, when I enter value and submit page, then the error should be cleared.', function() {
    //Given
    openQuestionnaire(radio_schema);

    //When
    RadioMandatoryPage.clickOther().submit();
    expect(RadioMandatoryPage.errorExists()).to.be.true
    RadioMandatoryPage.clickOther().setOtherInputField('Other Text').submit()

    //Then
    expect(RadioNonMandatoryPage.errorExists()).to.be.false
  })

  it('Given I have previously added text in other textfield and saved, when I change the answer to a different answer, then the text entered in other field must be wiped.', function() {
    //Given
    openQuestionnaire(radio_schema);

    //When
    RadioMandatoryPage.clickOther().setOtherInputField('Other Text').submit()
    RadioNonMandatoryPage.clickTopPrevious()
    RadioMandatoryPage.clickRadioMandatoryAnswerBacon().submit()
    RadioNonMandatoryPage.clickTopPrevious()

    //Then
    RadioMandatoryPage.clickOther()
    expect(RadioMandatoryPage.getOtherInputField()).to.equal('')
  })

  it('Given I have previously selected the None option and saved, When I return to the screen, Then my choice is remembered.', function() {
    // https://github.com/ONSdigital/eq-survey-runner/issues/1013
    // Given
    openQuestionnaire(radio_schema);

    expect(RadioMandatoryPage.RadioMandatoryAnswerNoneIsSelected()).to.be.false
    RadioMandatoryPage.clickRadioMandatoryAnswerNone()
    expect(RadioMandatoryPage.RadioMandatoryAnswerNoneIsSelected()).to.be.true
    RadioMandatoryPage.submit()

    // When
    RadioNonMandatoryPage.clickTopPrevious()

    // Then
    expect(RadioMandatoryPage.RadioMandatoryAnswerNoneIsSelected()).to.be.true
  })

  it('Given I have previously selected an option and saved, When I return to the screen and change my answer twice, Then my new choice is remembered and is shown on the Summary screen.', function() {
    // Given
    openQuestionnaire(radio_schema);

    // Nothing should be selected by default
    expect(RadioMandatoryPage.RadioMandatoryAnswerNoneIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerBaconIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerEggsIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerSausageIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerOtherIsSelected()).to.be.false

    // choose Eggs first
    RadioMandatoryPage.clickRadioMandatoryAnswerEggs()
    expect(RadioMandatoryPage.RadioMandatoryAnswerEggsIsSelected()).to.be.true
    RadioMandatoryPage.submit()

    // When I return to the screen
    RadioNonMandatoryPage.clickTopPrevious()

    // Then my choice is remembered (Eggs)
    expect(RadioMandatoryPage.RadioMandatoryAnswerNoneIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerBaconIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerEggsIsSelected()).to.be.true
    expect(RadioMandatoryPage.RadioMandatoryAnswerSausageIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerOtherIsSelected()).to.be.false

    // When I change my answer to the None option
    RadioMandatoryPage.clickRadioMandatoryAnswerNone()
    expect(RadioMandatoryPage.RadioMandatoryAnswerNoneIsSelected()).to.be.true
    expect(RadioMandatoryPage.RadioMandatoryAnswerBaconIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerEggsIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerSausageIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerOtherIsSelected()).to.be.false
    RadioMandatoryPage.submit()

    // Then my choice is remembered when I return
    RadioNonMandatoryPage.clickTopPrevious()
    expect(RadioMandatoryPage.RadioMandatoryAnswerNoneIsSelected()).to.be.true
    expect(RadioMandatoryPage.RadioMandatoryAnswerBaconIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerEggsIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerSausageIsSelected()).to.be.false
    expect(RadioMandatoryPage.RadioMandatoryAnswerOtherIsSelected()).to.be.false

    // When I change my answer for the last time to Sausage
    RadioMandatoryPage.clickRadioMandatoryAnswerSausage()

    // When I go to the summary
    RadioMandatoryPage.submit()

    // skipping non-mandatory page
    RadioNonMandatoryPage.submit()

    // Then my answer is shown
    expect(SummaryPage.getMandatoryAnswer()).to.contain('Sausage')
  })
})
