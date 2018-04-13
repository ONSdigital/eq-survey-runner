// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class HouseholdCompositionPage extends QuestionPage {

  constructor() {
    super('household-composition');
  }

  addPerson() {
    return 'button[name="action[add_answer]"]';
  }

  removePerson(index = 2) {
    return 'div:nth-child(' + index + ') > h3 > small > button';
  }

  numRemoveButtons() {
    return '[class="btn btn--link pluto"]';
  }

  firstName(index = '') {
    return '#household-0-first-name' + index ;
  }

  middleNames(index = '') {
    return '#household-0-middle-names' + index;
  }

  lastName(index = '') {
    return '#household-0-last-name' + index;
  }

  personLegend(index = 1) {
    return 'div:nth-child(' + index + ') > fieldset > legend';
  }

}
module.exports = new HouseholdCompositionPage();
