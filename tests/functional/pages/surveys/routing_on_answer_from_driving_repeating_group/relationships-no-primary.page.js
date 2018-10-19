// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RelationshipsNoPrimaryPage extends QuestionPage {

  constructor() {
    super('relationships-no-primary');
  }

  answer(instance) {
    return '[name="who-is-related-no-primary-' + instance + '"]';
  }

  relationship(instance, answer) {
    return '#who-is-related-no-primary-' + instance + ' > [value="' + answer + '"]';
  }

  answerLabel() { return '#label-who-is-related-no-primary'; }

}
module.exports = new RelationshipsNoPrimaryPage();
