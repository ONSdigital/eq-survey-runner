// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveTextfieldPage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-textfield');
  }

  textfield() {
    return '#textfield-answer';
  }

  textfieldLabel() { return '#label-textfield-answer'; }

  textfieldExclusiveIPreferNotToSay() {
    return '#textfield-exclusive-answer-0';
  }

  textfieldExclusiveIPreferNotToSayLabel() { return '#label-textfield-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveTextfieldPage();
