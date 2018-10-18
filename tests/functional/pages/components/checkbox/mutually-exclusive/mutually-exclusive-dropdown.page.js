// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveDropdownPage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-dropdown');
  }

  dropdown() {
    return '#dropdown-answer';
  }

  dropdownLabel() { return '#label-dropdown-answer'; }

  dropdownAnswer() {
    return '#dropdown-answer-0-answer';
  }

  dropdownExclusiveIPreferNotToSay() {
    return '#dropdown-exclusive-answer-0';
  }

  dropdownExclusiveIPreferNotToSayLabel() { return '#label-dropdown-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveDropdownPage();
