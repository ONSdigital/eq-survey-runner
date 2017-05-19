// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class MaritalStatusPage extends QuestionPage {

  constructor() {
    super('marital-status');
  }

  neverMarriedAndNeverRegisteredASameSexCivilPartnership() {
    return '#marital-status-answer-0';
  }

  married() {
    return '#marital-status-answer-1';
  }

  inARegisteredSameSexCivilPartnership() {
    return '#marital-status-answer-2';
  }

  separatedButStillLegallyMarried() {
    return '#marital-status-answer-3';
  }

  separatedButStillLegallyInASameSexCivilPartnership() {
    return '#marital-status-answer-4';
  }

  divorced() {
    return '#marital-status-answer-5';
  }

  formerlyInASameSexCivilPartnershipWhichIsNowLegallyDissolved() {
    return '#marital-status-answer-6';
  }

  widowed() {
    return '#marital-status-answer-7';
  }

  survivingPartnerFromASameSexCivilPartnership() {
    return '#marital-status-answer-8';
  }

}
module.exports = new MaritalStatusPage();
