// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class DropdownOptionalPage extends QuestionPage {

  constructor() {
    super('dropdown-optional');
  }

  answer() {
    return '#dropdown-optional-answer';
  }

  answerLabel() { return '#label-dropdown-optional-answer'; }

}
module.exports = new DropdownOptionalPage();
