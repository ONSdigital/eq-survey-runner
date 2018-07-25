// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class HouseholdCompositionPage extends QuestionPage {

  constructor() {
    super('household-composition');
  }

  addPerson() {
    return 'button[name="action[add_answer]"]';
  }

  removePerson(index = 0) {
    return 'div.question__answer:nth-child('+ (index+1) + ') > h3 > small > span > button';
    // Have to check whether it's visible in test code
  }

  personLegend(index = 1) {
    return 'div.question__answer:nth-child(' + index + ') > fieldset > legend';
  }
  answer(index = '') {
    return '#household-0-first-name' + index;
  }

}
module.exports = new HouseholdCompositionPage();
