// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  firstName(index = 0) { return '#first-name-' + index + '-answer'; }

  middleNames(index = 0) { return '#middle-names-' + index + '-answer'; }

  lastName(index = 0) { return '#last-name-' + index + '-answer'; }

  lastNameEdit(index = 0) { return '[data-qa="last-name-' + index + '-edit"]'; }

  multipleQuestionsGroupTitle(index = 0) { return '#multiple-questions-group-' + index; }

  whatIsYourAge(index = 0) { return '#what-is-your-age-' + index + '-answer'; }

  whatIsYourAgeEdit(index = 0) { return '[data-qa="what-is-your-age-' + index + '-edit"]'; }

  whatIsYourShoeSize(index = 0) { return '#what-is-your-shoe-size-' + index + '-answer'; }

  whatIsYourShoeSizeEdit(index = 0) { return '[data-qa="what-is-your-shoe-size-' + index + '-edit"]'; }

  confirmAnswer(index = 0) { return '#confirm-answer-' + index + '-answer'; }

  confirmAnswerEdit(index = 0) { return '[data-qa="confirm-answer-' + index + '-edit"]'; }

  repeatingGroupTitle(index = 0) { return '#repeating-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
