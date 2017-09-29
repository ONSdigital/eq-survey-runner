// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ImportancesInformationClientPage extends QuestionPage {

  constructor() {
    super('importances-information-client');
  }

  high() {
    return '#importances-information-client-answer-0';
  }

  highLabel() { return '#label-importances-information-client-answer-0'; }

  medium() {
    return '#importances-information-client-answer-1';
  }

  mediumLabel() { return '#label-importances-information-client-answer-1'; }

  low() {
    return '#importances-information-client-answer-2';
  }

  lowLabel() { return '#label-importances-information-client-answer-2'; }

  notImportant() {
    return '#importances-information-client-answer-3';
  }

  notImportantLabel() { return '#label-importances-information-client-answer-3'; }

}
module.exports = new ImportancesInformationClientPage();
