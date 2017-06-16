// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class VisitorUkResidentPage extends QuestionPage {

  constructor() {
    super('visitor-uk-resident');
  }

  yesUsuallyLivesInTheUnitedKingdom() {
    return '#visitor-uk-resident-answer-0';
  }

  other() {
    return '#visitor-uk-resident-answer-1';
  }

  otherText() {
    return '#visitor-uk-resident-answer-other';
  }

}
module.exports = new VisitorUkResidentPage();
