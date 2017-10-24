// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class InsuranceTypePage extends QuestionPage {

  constructor() {
    super('insurance-type');
  }

  buildings() {
    return '#insurance-type-answer-0';
  }

  buildingsLabel() { return '#label-insurance-type-answer-0'; }

  contents() {
    return '#insurance-type-answer-1';
  }

  contentsLabel() { return '#label-insurance-type-answer-1'; }

  both() {
    return '#insurance-type-answer-2';
  }

  bothLabel() { return '#label-insurance-type-answer-2'; }

}
module.exports = new InsuranceTypePage();
