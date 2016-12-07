import QuestionPage from '../../question.page'

class ContactDetailsPage extends QuestionPage {

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
