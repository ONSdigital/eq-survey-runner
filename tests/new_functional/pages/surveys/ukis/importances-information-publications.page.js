// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ImportancesInformationPublicationsPage extends QuestionPage {

  constructor() {
    super('importances-information-publications');
  }

  high() {
    return '#importances-information-publications-answer-0';
  }

  highLabel() { return '#label-importances-information-publications-answer-0'; }

  medium() {
    return '#importances-information-publications-answer-1';
  }

  mediumLabel() { return '#label-importances-information-publications-answer-1'; }

  low() {
    return '#importances-information-publications-answer-2';
  }

  lowLabel() { return '#label-importances-information-publications-answer-2'; }

  notImportant() {
    return '#importances-information-publications-answer-3';
  }

  notImportantLabel() { return '#label-importances-information-publications-answer-3'; }

}
module.exports = new ImportancesInformationPublicationsPage();
