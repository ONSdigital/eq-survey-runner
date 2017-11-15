// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class HouseholdCompositionPage extends QuestionPage {

  constructor() {
    super('household-composition');
  }

  addPerson() {
    return 'button[name="action[add_answer]"]';
  }

  removePerson(index) {
    return 'button[value="' + index + '"]';
    // Have to check whether it's visible in test code
  }

  firstName(index = 0) {
    return '#household-' + index + '-first-name';
  }

  middleNames(index = 0) {
    return '#household-' + index + '-middle-names';
  }

  lastName(index = 0) {
    return '#household-' + index + '-last-name';
  }

}
module.exports = new HouseholdCompositionPage();
