// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class UsualResidentsPage extends QuestionPage {

  constructor() {
    super('usual-residents');
  }

  yes() {
    return '#usual-residents-answer-0';
  }

  yesLabel() { return '#label-usual-residents-answer-0'; }

  no() {
    return '#usual-residents-answer-1';
  }

  noLabel() { return '#label-usual-residents-answer-1'; }

}
module.exports = new UsualResidentsPage();
