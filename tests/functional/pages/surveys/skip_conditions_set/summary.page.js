// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  foodAnswer(index = 0) { return '#food-answer-' + index + '-answer'; }

  foodAnswerEdit(index = 0) { return '[data-qa="food-answer-' + index + '-edit"]'; }

  drinkAnswer(index = 0) { return '#drink-answer-' + index + '-answer'; }

  drinkAnswerEdit(index = 0) { return '[data-qa="drink-answer-' + index + '-edit"]'; }

  breakfastTitle(index = 0) { return '#breakfast-' + index; }

}
module.exports = new SummaryPage();
