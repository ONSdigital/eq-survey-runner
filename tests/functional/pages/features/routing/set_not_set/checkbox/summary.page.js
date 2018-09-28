// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  otherAnswerTopping() { return '#other-answer-topping-answer'; }

  otherAnswerToppingEdit() { return '[data-qa="other-answer-topping-edit"]'; }

  optionalMutuallyExclusiveAnswer() { return '#optional-mutually-exclusive-answer-answer'; }

  optionalMutuallyExclusiveAnswerEdit() { return '[data-qa="optional-mutually-exclusive-answer-edit"]'; }

  checkboxesTitle() { return '#checkboxes'; }

}
module.exports = new SummaryPage();
