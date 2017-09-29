// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ImportancesInformationConsultantsPage extends QuestionPage {

  constructor() {
    super('importances-information-consultants');
  }

  high() {
    return '#importances-information-consultants-answer-0';
  }

  highLabel() { return '#label-importances-information-consultants-answer-0'; }

  medium() {
    return '#importances-information-consultants-answer-1';
  }

  mediumLabel() { return '#label-importances-information-consultants-answer-1'; }

  low() {
    return '#importances-information-consultants-answer-2';
  }

  lowLabel() { return '#label-importances-information-consultants-answer-2'; }

  notImportant() {
    return '#importances-information-consultants-answer-3';
  }

  notImportantLabel() { return '#label-importances-information-consultants-answer-3'; }

}
module.exports = new ImportancesInformationConsultantsPage();
