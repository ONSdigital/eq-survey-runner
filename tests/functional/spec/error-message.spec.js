import chai from 'chai'
import {getRandomString} from '../helpers'
import devPage from '../pages/dev.page'
import landingPage from '../pages/landing.page'
import monthlyBusinessSurveyPage from '../pages/surveys/monthly-business-survey.page'

const expect = chai.expect

describe('Error messages', function() {
  before('Progress to tge correct page', function() {
    devPage.open()
      .setUserId(getRandomString(10))
      .setCollectionId(getRandomString(3))
      .setSchema('1_0205.json')
      .submit()
    landingPage.getStarted()
  })

  it('Given the survey contains errors when the error link is clicked then the day input field is focused', function() {
    monthlyBusinessSurveyPage.setFromSalesPeriodDay('01')
      .setFromSalesPeriodYear('2016')
      .setToSalesPeriodDay('01')
      .setToSalesPeriodYear('2016')
      .submit()

    monthlyBusinessSurveyPage.focusErrorField()

    expect(getElementId(browser.elementActive())).to.equal(getElementId(monthlyBusinessSurveyPage.getFromSalesPeriodDay()))
  })

  function getElementId(element) {
    return browser.elementIdAttribute(element.value.ELEMENT, "id").value
  }

})
