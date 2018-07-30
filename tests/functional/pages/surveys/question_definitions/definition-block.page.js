// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class DefinitionBlockPage extends QuestionPage {

  constructor() {
    super('definition-block');
  }

  definitionTitle1() { return '[data-definition-title-index="1"]'; }

  definitionContent1() { return '[data-definition-content-index="1"]'; }

  definitionButton1() { return '[data-definition-hide-button-index="1"]'; }

  definitionTitle2() { return '[data-definition-title-index="2"]'; }

  definitionContent2() { return '[data-definition-content-index="2"]'; }

  definitionButton2() { return '[data-definition-hide-button-index="2"]'; }

  yes() {
    return '#radio-mandatory-answer-0';
  }

  yesLabel() { return '#label-radio-mandatory-answer-0'; }

  no() {
    return '#radio-mandatory-answer-1';
  }

  noLabel() { return '#label-radio-mandatory-answer-1'; }

}
module.exports = new DefinitionBlockPage();
