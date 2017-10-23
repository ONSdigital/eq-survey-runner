// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class TypeOfHousePage extends QuestionPage {

  constructor() {
    super('type-of-house');
  }

  detached() {
    return '#type-of-house-answer-0';
  }

  semiDetached() {
    return '#type-of-house-answer-1';
  }

  terraced() {
    return '#type-of-house-answer-2';
  }

}
module.exports = new TypeOfHousePage();
