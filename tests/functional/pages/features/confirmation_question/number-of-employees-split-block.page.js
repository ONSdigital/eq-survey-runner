// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class NumberOfEmployeesSplitBlockPage extends QuestionPage {

  constructor() {
    super('number-of-employees-split-block');
  }

  numberOfEmployeesMaleMore30Hours() {
    return '#number-of-employees-male-more-30-hours';
  }

  numberOfEmployeesMaleMore30HoursLabel() { return '#label-number-of-employees-male-more-30-hours'; }

  numberOfEmployeesFemaleMore30Hours() {
    return '#number-of-employees-female-more-30-hours';
  }

  numberOfEmployeesFemaleMore30HoursLabel() { return '#label-number-of-employees-female-more-30-hours'; }

}
module.exports = new NumberOfEmployeesSplitBlockPage();
