// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  noOfRepeatsAnswer() { return '#no-of-repeats-answer-answer'; }

  noOfRepeatsAnswerEdit() { return '[data-qa="no-of-repeats-answer-edit"]'; }

  conditionalAnswer() { return '#conditional-answer-answer'; }

  conditionalAnswerEdit() { return '[data-qa="conditional-answer-edit"]'; }

  whatIsYourAge() { return '#what-is-your-age-answer'; }

  whatIsYourAgeEdit() { return '[data-qa="what-is-your-age-edit"]'; }

  whatIsYourShoeSize() { return '#what-is-your-shoe-size-answer'; }

  whatIsYourShoeSizeEdit() { return '[data-qa="what-is-your-shoe-size-edit"]'; }

}
module.exports = new SummaryPage();
