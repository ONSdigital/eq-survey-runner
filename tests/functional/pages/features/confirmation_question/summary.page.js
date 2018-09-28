// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  numberOfEmployeesTotal(index = 0) { return '#number-of-employees-total-' + index + '-answer'; }

  numberOfEmployeesTotalEdit(index = 0) { return '[data-qa="number-of-employees-total-' + index + '-edit"]'; }

  confirmZeroEmployeesAnswer(index = 0) { return '#confirm-zero-employees-answer-' + index + '-answer'; }

  confirmZeroEmployeesAnswerEdit(index = 0) { return '[data-qa="confirm-zero-employees-answer-' + index + '-edit"]'; }

  numberOfEmployeesMaleMore30Hours(index = 0) { return '#number-of-employees-male-more-30-hours-' + index + '-answer'; }

  numberOfEmployeesMaleMore30HoursEdit(index = 0) { return '[data-qa="number-of-employees-male-more-30-hours-' + index + '-edit"]'; }

  numberOfEmployeesFemaleMore30Hours(index = 0) { return '#number-of-employees-female-more-30-hours-' + index + '-answer'; }

  numberOfEmployeesFemaleMore30HoursEdit(index = 0) { return '[data-qa="number-of-employees-female-more-30-hours-' + index + '-edit"]'; }

  confirmationBlockTitle(index = 0) { return '#confirmation-block-' + index; }

}
module.exports = new SummaryPage();
