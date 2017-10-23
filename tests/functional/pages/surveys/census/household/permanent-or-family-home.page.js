// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class PermanentOrFamilyHomePage extends QuestionPage {

  constructor() {
    super('permanent-or-family-home');
  }

  yes() {
    return '#permanent-or-family-home-answer-0';
  }

  no() {
    return '#permanent-or-family-home-answer-1';
  }

}
module.exports = new PermanentOrFamilyHomePage();
