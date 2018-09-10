// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  feelingAnswer(index = 0) { return '#feeling-answer-' + index + '-answer'; }

  feelingAnswerEdit(index = 0) { return '[data-qa="feeling-answer-' + index + '-edit"]'; }

  behalfOfAnswer(index = 0) { return '#behalf-of-answer-' + index + '-answer'; }

  behalfOfAnswerEdit(index = 0) { return '[data-qa="behalf-of-answer-' + index + 'edit"]'; }

  genderAnswer(index = 0) { return '#gender-answer-' + index + '-answer'; }

  genderAnswerEdit(index = 0) { return '[data-qa="gender-answer-' + index + '-edit"]'; }

  ageAnswer(index = 0) { return '#age-answer-' + index + '-answer'; }

  ageAnswerEdit(index = 0) { return '[data-qa="age-answer-' + index + '-edit"]'; }

  sureAnswer(index = 0) { return '#sure-answer-' + index + '-answer'; }

  sureAnswerEdit(index = 0) { return '[data-qa="sure-answer-' + index + '-edit"]'; }

  groupTitle(index = 0) { return '#group-' + index; }

}
module.exports = new SummaryPage();
