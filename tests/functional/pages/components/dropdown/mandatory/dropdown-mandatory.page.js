// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class DropdownMandatoryPage extends QuestionPage {

  constructor() {
    super('dropdown-mandatory');
  }

  answer() {
    return '#dropdown-mandatory-answer';
  }

  answerLabel() { return '#label-dropdown-mandatory-answer'; }

}
module.exports = new DropdownMandatoryPage();
