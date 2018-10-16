// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  primaryName(index = 0) { return '#primary-name-' + index + '-answer'; }

  primaryNameEdit(index = 0) { return '[data-qa="primary-name-' + index + '-edit"]'; }

  primaryNameQuestion(index = 0) { return '#primary-name-question-' + index; }

  primaryGroupTitle(index = 0) { return '#primary-group-' + index; }

  repeatingAnyoneElse(index = 0) { return '#repeating-anyone-else-' + index + '-answer'; }

  repeatingAnyoneElseEdit(index = 0) { return '[data-qa="repeating-anyone-else-' + index + '-edit"]'; }

  repeatingAnyoneElseQuestion(index = 0) { return '#repeating-anyone-else-question-' + index; }

  repeatingName(index = 0) { return '#repeating-name-' + index + '-answer'; }

  repeatingNameEdit(index = 0) { return '[data-qa="repeating-name-' + index + '-edit"]'; }

  repeatingNameQuestion(index = 0) { return '#repeating-name-question-' + index; }

  repeatingGroupTitle(index = 0) { return '#repeating-group-' + index; }

  groupLessThan2Answer(index = 0) { return '#group-less-than-2-answer-' + index + '-answer'; }

  groupLessThan2AnswerEdit(index = 0) { return '[data-qa="group-less-than-2-answer-' + index + '-edit"]'; }

  groupLessThan2Question(index = 0) { return '#group-less-than-2-question-' + index; }

  groupLessThan2Title(index = 0) { return '#group-less-than-2-' + index; }

  groupEqual2Answer(index = 0) { return '#group-equal-2-answer-' + index + '-answer'; }

  groupEqual2AnswerEdit(index = 0) { return '[data-qa="group-equal-2-answer-' + index + '-edit"]'; }

  groupEqual2Question(index = 0) { return '#group-equal-2-question-' + index; }

  groupEqual2Title(index = 0) { return '#group-equal-2-' + index; }

  groupGreaterThan2Answer(index = 0) { return '#group-greater-than-2-answer-' + index + '-answer'; }

  groupGreaterThan2AnswerEdit(index = 0) { return '[data-qa="group-greater-than-2-answer-' + index + '-edit"]'; }

  groupGreaterThan2Question(index = 0) { return '#group-greater-than-2-question-' + index; }

  groupGreaterThan2Title(index = 0) { return '#group-greater-than-2-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
