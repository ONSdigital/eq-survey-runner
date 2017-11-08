// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class TextfieldPage extends QuestionPage {

  constructor() {
    super('textfield');
  }

  firstText() {
    return '#first-text';
  }

  firstTextLabel() { return '#label-first-text'; }

  secondText() {
    return '#second-text';
  }

  secondTextLabel() { return '#label-second-text'; }

}
module.exports = new TextfieldPage();
