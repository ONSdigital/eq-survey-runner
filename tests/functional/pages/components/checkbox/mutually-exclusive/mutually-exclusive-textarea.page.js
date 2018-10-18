// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveTextareaPage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-textarea');
  }

  textarea() {
    return '#textarea-answer';
  }

  textareaLabel() { return '#label-textarea-answer'; }

  textareaExclusiveIPreferNotToSay() {
    return '#textarea-exclusive-answer-0';
  }

  textareaExclusiveIPreferNotToSayLabel() { return '#label-textarea-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveTextareaPage();
