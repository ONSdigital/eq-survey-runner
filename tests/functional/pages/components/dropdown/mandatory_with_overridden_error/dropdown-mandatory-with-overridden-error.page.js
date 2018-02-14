// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class DropdownMandatoryWithOverriddenErrorPage extends QuestionPage {

  constructor() {
    super('dropdown-mandatory-with-overridden-error');
  }

  answer() {
    return '#dropdown-mandatory-with-overridden-answer';
  }

  answerLabel() { return '#label-dropdown-mandatory-with-overridden-answer'; }

}
module.exports = new DropdownMandatoryWithOverriddenErrorPage();
