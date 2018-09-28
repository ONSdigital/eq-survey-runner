// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  totalAnswer(index = 0) { return '#total-answer-' + index + '-answer'; }

  totalAnswerEdit(index = 0) { return '[data-qa="total-answer-' + index + '-edit"]'; }

  breakdown1(index = 0) { return '#breakdown-1-' + index + '-answer'; }

  breakdown1Edit(index = 0) { return '[data-qa="breakdown-1-' + index + '-edit"]'; }

  breakdown2(index = 0) { return '#breakdown-2-' + index + '-answer'; }

  breakdown2Edit(index = 0) { return '[data-qa="breakdown-2-' + index + '-edit"]'; }

  breakdown3(index = 0) { return '#breakdown-3-' + index + '-answer'; }

  breakdown3Edit(index = 0) { return '[data-qa="breakdown-3-' + index + '-edit"]'; }

  breakdown4(index = 0) { return '#breakdown-4-' + index + '-answer'; }

  breakdown4Edit(index = 0) { return '[data-qa="breakdown-4-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
