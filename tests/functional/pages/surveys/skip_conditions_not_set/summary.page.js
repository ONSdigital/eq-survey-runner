// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  foodAnswer() { return '#food-answer-answer'; }

  foodAnswerEdit() { return '[data-qa="food-answer-edit"]'; }

  drinkAnswer() { return '#drink-answer-answer'; }

  drinkAnswerEdit() { return '[data-qa="drink-answer-edit"]'; }

  sandwichAnswer() { return '#sandwich-answer-answer'; }

  sandwichAnswerEdit() { return '[data-qa="sandwich-answer-edit"]'; }

  breakfastTitle() { return '#breakfast'; }

}
module.exports = new SummaryPage();
