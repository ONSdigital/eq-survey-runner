// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class HouseTypePage extends QuestionPage {

  constructor() {
    super('house-type');
  }

  detached() {
    return '#house-type-answer-0';
  }

  detachedLabel() { return '#label-house-type-answer-0'; }

  semiDetached() {
    return '#house-type-answer-1';
  }

  semiDetachedLabel() { return '#label-house-type-answer-1'; }

  terrace() {
    return '#house-type-answer-2';
  }

  terraceLabel() { return '#label-house-type-answer-2'; }

}
module.exports = new HouseTypePage();
