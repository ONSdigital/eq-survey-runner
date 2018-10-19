// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SexBlockNoPrimaryPage extends QuestionPage {

  constructor() {
    super('sex-block-no-primary');
  }

  male() {
    return '#sex-answer-no-primary-0';
  }

  maleLabel() { return '#label-sex-answer-no-primary-0'; }

  female() {
    return '#sex-answer-no-primary-1';
  }

  femaleLabel() { return '#label-sex-answer-no-primary-1'; }

}
module.exports = new SexBlockNoPrimaryPage();
