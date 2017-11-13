// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class SexPage extends QuestionPage {

  constructor() {
    super('sex');
  }

  heterosexualOrStraight() {
    return '#sex-answer-0';
  }

  heterosexualOrStraightLabel() { return '#label-sex-answer-0'; }

  gayOrLesbian() {
    return '#sex-answer-1';
  }

  gayOrLesbianLabel() { return '#label-sex-answer-1'; }

  bisexual() {
    return '#sex-answer-2';
  }

  bisexualLabel() { return '#label-sex-answer-2'; }

  other() {
    return '#sex-answer-3';
  }

  otherLabel() { return '#label-sex-answer-3'; }

  preferNotToSay() {
    return '#sex-answer-4';
  }

  preferNotToSayLabel() { return '#label-sex-answer-4'; }

}
module.exports = new SexPage();
