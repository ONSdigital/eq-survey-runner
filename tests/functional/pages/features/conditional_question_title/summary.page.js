// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  feelingAnswer() { return '#feeling-answer-answer'; }

  feelingAnswerEdit() { return '[data-qa="feeling-answer-edit"]'; }

  behalfOfAnswer() { return '#behalf-of-answer-answer'; }

  behalfOfAnswerEdit() { return '[data-qa="behalf-of-answer-edit"]'; }

  genderAnswer() { return '#gender-answer-answer'; }

  genderAnswerEdit() { return '[data-qa="gender-answer-edit"]'; }

  ageAnswer() { return '#age-answer-answer'; }

  ageAnswerEdit() { return '[data-qa="age-answer-edit"]'; }

  sureAnswer() { return '#sure-answer-answer'; }

  sureAnswerEdit() { return '[data-qa="sure-answer-edit"]'; }

  groupTitle() { return '#group'; }

}
module.exports = new SummaryPage();
