// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class HowLongPage extends QuestionPage {

  constructor() {
    super('how-long')
  }

  setGeneralInformationHoursAnswer(value) {
    browser.setValue('[name="general-information-hours-answer"]', value)
    return this
  }

  getGeneralInformationHoursAnswer(value) {
    return browser.element('[name="general-information-hours-answer"]').getValue()
  }

  setHowLongMinutesAnswer(value) {
    browser.setValue('[name="how-long-minutes-answer"]', value)
    return this
  }

  getHowLongMinutesAnswer(value) {
    return browser.element('[name="how-long-minutes-answer"]').getValue()
  }

}

export default new HowLongPage()
