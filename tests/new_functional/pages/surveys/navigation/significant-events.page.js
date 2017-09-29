// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SignificantEventsPage extends QuestionPage {

  constructor() {
    super('significant-events');
  }

  establishedYes() {
    return '#significant-events-established-answer-0';
  }

  establishedYesLabel() { return '#label-significant-events-established-answer-0'; }

  establishedNo() {
    return '#significant-events-established-answer-1';
  }

  establishedNoLabel() { return '#label-significant-events-established-answer-1'; }

  turnoverIncreaseYes() {
    return '#significant-events-turnover-increase-answer-0';
  }

  turnoverIncreaseYesLabel() { return '#label-significant-events-turnover-increase-answer-0'; }

  turnoverIncreaseNo() {
    return '#significant-events-turnover-increase-answer-1';
  }

  turnoverIncreaseNoLabel() { return '#label-significant-events-turnover-increase-answer-1'; }

  turnoverDecreaseYes() {
    return '#significant-events-turnover-decrease-answer-0';
  }

  turnoverDecreaseYesLabel() { return '#label-significant-events-turnover-decrease-answer-0'; }

  turnoverDecreaseNo() {
    return '#significant-events-turnover-decrease-answer-1';
  }

  turnoverDecreaseNoLabel() { return '#label-significant-events-turnover-decrease-answer-1'; }

}
module.exports = new SignificantEventsPage();
