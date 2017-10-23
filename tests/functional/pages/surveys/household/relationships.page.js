// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RelationshipsPage extends QuestionPage {

  constructor() {
    super('relationships');
  }

  answer(instance = 0) {
    return '[name="who-is-related-' + instance + '"]';
  }

  relationship(instance = 0, answer = 'Husband or wife') {
    return '#who-is-related-' + instance + ' > [value="' + answer + '"]';
  }

  answerLabel() { return '#label-who-is-related'; }

}
module.exports = new RelationshipsPage();
