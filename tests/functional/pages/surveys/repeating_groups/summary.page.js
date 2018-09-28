// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  noOfRepeatsAnswer(index = 0) { return '#no-of-repeats-answer-' + index + '-answer'; }

  noOfRepeatsAnswerEdit(index = 0) { return '[data-qa="no-of-repeats-answer-' + index + '-edit"]'; }

  conditionalAnswer(index = 0) { return '#conditional-answer-' + index + '-answer'; }

  conditionalAnswerEdit(index = 0) { return '[data-qa="conditional-answer-' + index + '-edit"]'; }

  whatIsYourAge(index = 0) { return '#what-is-your-age-' + index + '-answer'; }

  whatIsYourAgeEdit(index = 0) { return '[data-qa="what-is-your-age-' + index + '-edit"]'; }

  whatIsYourShoeSize(index = 0) { return '#what-is-your-shoe-size-' + index + '-answer'; }

  whatIsYourShoeSizeEdit(index = 0) { return '[data-qa="what-is-your-shoe-size-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
