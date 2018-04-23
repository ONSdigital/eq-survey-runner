// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

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
  firstName(index = '') {
    return '#household-0-first-name' + index;
  }

  middleNames(index = '') {
    return '#household-0-middle-names' + index;
  }

  lastName(index = '') {
    return '#household-0-last-name' + index;
  }

}
module.exports = new HouseholdCompositionPage();
