// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class PrimaryLiveHereBlockPage extends QuestionPage {

  constructor() {
    super('primary-live-here-block');
  }

  yes() {
    return '#primary-live-here-0';
  }

  yesLabel() { return '#label-primary-live-here-0'; }

  no() {
    return '#primary-live-here-1';
  }

  noLabel() { return '#label-primary-live-here-1'; }

}
module.exports = new PrimaryLiveHereBlockPage();
