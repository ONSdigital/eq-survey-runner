// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SetDurationUnitsBlockPage extends QuestionPage {

  constructor() {
    super('set-duration-units-block');
  }

  durationHour() {
    return '#duration-hour';
  }

  durationHourLabel() { return '#label-duration-hour'; }

  durationHourUnit() {
    return '#duration-hour-type';
  }

  durationYear() {
    return '#duration-year';
  }

  durationYearLabel() { return '#label-duration-year'; }

  durationYearUnit() {
    return '#duration-year-type';
  }

}
module.exports = new SetDurationUnitsBlockPage();
