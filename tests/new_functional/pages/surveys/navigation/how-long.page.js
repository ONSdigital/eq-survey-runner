// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class HowLongPage extends QuestionPage {

  constructor() {
    super('how-long');
  }

  generalInformationHours() {
    return '#general-information-hours-answer';
  }

  generalInformationHoursLabel() { return '#label-general-information-hours-answer'; }

  minutes() {
    return '#how-long-minutes-answer';
  }

  minutesLabel() { return '#label-how-long-minutes-answer'; }

}
module.exports = new HowLongPage();
