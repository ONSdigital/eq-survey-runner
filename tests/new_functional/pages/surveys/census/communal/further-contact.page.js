// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class FurtherContactPage extends QuestionPage {

  constructor() {
    super('further-contact');
  }

  yes() {
    return '#further-contact-answer-0';
  }

  yesLabel() { return '#label-further-contact-answer-0'; }

  no() {
    return '#further-contact-answer-1';
  }

  noLabel() { return '#label-further-contact-answer-1'; }

}
module.exports = new FurtherContactPage();
