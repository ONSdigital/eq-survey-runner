// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class HouseholdSummaryPage extends QuestionPage {

  constructor() {
    super('household-summary');
  }

  yes() {
    return '#household-composition-add-another-0';
  }

  yesLabel() { return '#label-household-composition-add-another-0'; }

  no() {
    return '#household-composition-add-another-1';
  }

  noLabel() { return '#label-household-composition-add-another-1'; }

  houseIncludes(index = 1) { return 'div.block__description.mars > ul > li:nth-child('+ index +')'; }

}
module.exports = new HouseholdSummaryPage();
