// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class ContactDetailsPage extends QuestionPage {

  constructor() {
    super('contact-details');
  }

  name() {
    return '#contact-details-answer-name';
  }

  nameLabel() { return '#label-contact-details-answer-name'; }

  email() {
    return '#contact-details-answer-email';
  }

  emailLabel() { return '#label-contact-details-answer-email'; }

  phone() {
    return '#contact-details-answer-phone';
  }

  phoneLabel() { return '#label-contact-details-answer-phone'; }

}
module.exports = new ContactDetailsPage();
