// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RepeatingBlock1Page extends QuestionPage {

  constructor() {
    super('repeating-block-1');
  }

  yes() {
    return '#what-is-your-age-0';
  }

  yesLabel() { return '#label-what-is-your-age-0'; }

  no() {
    return '#what-is-your-age-1';
  }

  noLabel() { return '#label-what-is-your-age-1'; }

}
module.exports = new RepeatingBlock1Page();
