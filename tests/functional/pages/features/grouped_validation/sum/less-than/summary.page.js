// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  totalAnswer() { return '#total-answer-answer'; }

  totalAnswerEdit() { return '[data-qa="total-answer-edit"]'; }

  breakdown1() { return '#breakdown-1-answer'; }

  breakdown1Edit() { return '[data-qa="breakdown-1-edit"]'; }

  breakdown2() { return '#breakdown-2-answer'; }

  breakdown2Edit() { return '[data-qa="breakdown-2-edit"]'; }

  breakdown3() { return '#breakdown-3-answer'; }

  breakdown3Edit() { return '[data-qa="breakdown-3-edit"]'; }

  breakdown4() { return '#breakdown-4-answer'; }

  breakdown4Edit() { return '[data-qa="breakdown-4-edit"]'; }

}
module.exports = new SummaryPage();
