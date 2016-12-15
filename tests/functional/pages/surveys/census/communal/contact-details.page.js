// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:19:14.091677 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class ContactDetailsPage extends QuestionPage {

  constructor() {
    super('contact-details')
  }

  setContactDetailsAnswerName(value) {
    browser.setValue('[name="contact-details-answer-name"]', value)
    return this
  }

  getContactDetailsAnswerName(value) {
    return browser.element('[name="contact-details-answer-name"]').getValue()
  }

  setContactDetailsAnswerEmail(value) {
    browser.setValue('[name="contact-details-answer-email"]', value)
    return this
  }

  getContactDetailsAnswerEmail(value) {
    return browser.element('[name="contact-details-answer-email"]').getValue()
  }

  setContactDetailsAnswerPhone(value) {
    browser.setValue('[name="contact-details-answer-phone"]', value)
    return this
  }

  getContactDetailsAnswerPhone(value) {
    return browser.element('[name="contact-details-answer-phone"]').getValue()
  }

}

export default new ContactDetailsPage()
