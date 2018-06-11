// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class MultipleQuestionVersionsBlockPage extends QuestionPage {

  constructor() {
    super('multiple-question-versions-block');
  }

  genderMale() {
    return '#gender-answer-0';
  }

  genderMaleLabel() { return '#label-gender-answer-0'; }

  genderFemale() {
    return '#gender-answer-1';
  }

  genderFemaleLabel() { return '#label-gender-answer-1'; }

  age() {
    return '#age-answer';
  }

  ageLabel() { return '#label-age-answer'; }

  sureYes() {
    return '#sure-answer-0';
  }

  sureYesLabel() { return '#label-sure-answer-0'; }

  sureNo() {
    return '#sure-answer-1';
  }

  sureNoLabel() { return '#label-sure-answer-1'; }

}
module.exports = new MultipleQuestionVersionsBlockPage();
