// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class SexualIdentityPage extends QuestionPage {

  constructor() {
    super('sexual-identity');
  }

  heterosexualOrStraight() {
    return '#sexual-identity-answer-0';
  }

  heterosexualOrStraightLabel() { return '#label-sexual-identity-answer-0'; }

  gayOrLesbian() {
    return '#sexual-identity-answer-1';
  }

  gayOrLesbianLabel() { return '#label-sexual-identity-answer-1'; }

  bisexual() {
    return '#sexual-identity-answer-2';
  }

  bisexualLabel() { return '#label-sexual-identity-answer-2'; }

  other() {
    return '#sexual-identity-answer-3';
  }

  otherLabel() { return '#label-sexual-identity-answer-3'; }

  otherText() {
    return '#sexual-identity-answer-other';
  }

  preferNotToSay() {
    return '#sexual-identity-answer-4';
  }

  preferNotToSayLabel() { return '#label-sexual-identity-answer-4'; }

}
module.exports = new SexualIdentityPage();
