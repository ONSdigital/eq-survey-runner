// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  numberOfEmployeesTotal() { return '#number-of-employees-total-answer'; }

  numberOfEmployeesTotalEdit() { return '[data-qa="number-of-employees-total-edit"]'; }

  confirmZeroEmployeesAnswer() { return '#confirm-zero-employees-answer-answer'; }

  confirmZeroEmployeesAnswerEdit() { return '[data-qa="confirm-zero-employees-answer-edit"]'; }

  numberOfEmployeesMaleMore30Hours() { return '#number-of-employees-male-more-30-hours-answer'; }

  numberOfEmployeesMaleMore30HoursEdit() { return '[data-qa="number-of-employees-male-more-30-hours-edit"]'; }

  numberOfEmployeesFemaleMore30Hours() { return '#number-of-employees-female-more-30-hours-answer'; }

  numberOfEmployeesFemaleMore30HoursEdit() { return '[data-qa="number-of-employees-female-more-30-hours-edit"]'; }

  confirmationBlockTitle() { return '#confirmation-block'; }

}
module.exports = new SummaryPage();
