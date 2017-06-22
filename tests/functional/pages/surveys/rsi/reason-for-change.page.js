// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ReasonForChangePage extends MultipleChoiceWithOtherPage {
  constructor() {
    super('reason-for-change')
  }
  clickReasonForChangeAnswerInStoreOnlinePromotions() {
    browser.element('[id="reason-for-change-answer-0"]').click()
    return this
  }
  ReasonForChangeAnswerInStoreOnlinePromotionsIsSelected() {
    return browser.element('[id="reason-for-change-answer-0"]').isSelected()
  }
  clickReasonForChangeAnswerSpecialEventsEGSportingEvents() {
    browser.element('[id="reason-for-change-answer-1"]').click()
    return this
  }
  ReasonForChangeAnswerSpecialEventsEGSportingEventsIsSelected() {
    return browser.element('[id="reason-for-change-answer-1"]').isSelected()
  }
  clickReasonForChangeAnswerCalendarEventsEGChristmasEasterBankHoliday() {
    browser.element('[id="reason-for-change-answer-2"]').click()
    return this
  }
  ReasonForChangeAnswerCalendarEventsEGChristmasEasterBankHolidayIsSelected() {
    return browser.element('[id="reason-for-change-answer-2"]').isSelected()
  }
  clickReasonForChangeAnswerWeather() {
    browser.element('[id="reason-for-change-answer-3"]').click()
    return this
  }
  ReasonForChangeAnswerWeatherIsSelected() {
    return browser.element('[id="reason-for-change-answer-3"]').isSelected()
  }
  clickReasonForChangeAnswerStoreClosures() {
    browser.element('[id="reason-for-change-answer-4"]').click()
    return this
  }
  ReasonForChangeAnswerStoreClosuresIsSelected() {
    return browser.element('[id="reason-for-change-answer-4"]').isSelected()
  }
  clickReasonForChangeAnswerStoreOpenings() {
    browser.element('[id="reason-for-change-answer-5"]').click()
    return this
  }
  ReasonForChangeAnswerStoreOpeningsIsSelected() {
    return browser.element('[id="reason-for-change-answer-5"]').isSelected()
  }
  clickReasonForChangeAnswerOther() {
    browser.element('[id="reason-for-change-answer-6"]').click()
    return this
  }
  ReasonForChangeAnswerOtherIsSelected() {
    return browser.element('[id="reason-for-change-answer-6"]').isSelected()
  }
}

export default new ReasonForChangePage()
