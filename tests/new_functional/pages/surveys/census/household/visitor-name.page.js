// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class VisitorNamePage extends QuestionPage {

  constructor() {
    super('visitor-name');
  }

  visitorFirstName() {
    return '#visitor-first-name';
  }

  visitorFirstNameLabel() { return '#label-visitor-first-name'; }

  visitorLastName() {
    return '#visitor-last-name';
  }

  visitorLastNameLabel() { return '#label-visitor-last-name'; }

}
module.exports = new VisitorNamePage();
