// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ImportancesInformationGovernmentPage extends QuestionPage {

  constructor() {
    super('importances-information-government');
  }

  high() {
    return '#importances-information-government-answer-0';
  }

  highLabel() { return '#label-importances-information-government-answer-0'; }

  medium() {
    return '#importances-information-government-answer-1';
  }

  mediumLabel() { return '#label-importances-information-government-answer-1'; }

  low() {
    return '#importances-information-government-answer-2';
  }

  lowLabel() { return '#label-importances-information-government-answer-2'; }

  notImportant() {
    return '#importances-information-government-answer-3';
  }

  notImportantLabel() { return '#label-importances-information-government-answer-3'; }

}
module.exports = new ImportancesInformationGovernmentPage();
