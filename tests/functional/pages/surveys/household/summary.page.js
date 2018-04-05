// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  lastName() { return '#last-name-answer'; }

  lastNameEdit() { return '[data-qa="last-name-edit"]'; }

  multipleQuestionsGroupTitle() { return '#multiple-questions-group'; }

  whatIsYourAge() { return '#what-is-your-age-answer'; }

  whatIsYourAgeEdit() { return '[data-qa="what-is-your-age-edit"]'; }

  whatIsYourShoeSize() { return '#what-is-your-shoe-size-answer'; }

  whatIsYourShoeSizeEdit() { return '[data-qa="what-is-your-shoe-size-edit"]'; }

  confirmAnswer() { return '#confirm-answer-answer'; }

  confirmAnswerEdit() { return '[data-qa="confirm-answer-edit"]'; }

  repeatingGroupTitle() { return '#repeating-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
