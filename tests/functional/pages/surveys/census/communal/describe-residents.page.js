// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class DescribeResidentsPage extends QuestionPage {

  constructor() {
    super('describe-residents');
  }

  familyMembers() {
    return '#describe-residents-answer-0';
  }

  familyMembersLabel() { return '#label-describe-residents-answer-0'; }

  payingGuests() {
    return '#describe-residents-answer-1';
  }

  payingGuestsLabel() { return '#label-describe-residents-answer-1'; }

  staff() {
    return '#describe-residents-answer-2';
  }

  staffLabel() { return '#label-describe-residents-answer-2'; }

  other() {
    return '#describe-residents-answer-3';
  }

  otherLabel() { return '#label-describe-residents-answer-3'; }

  otherText() {
    return '#describe-residents-answer-other';
  }

}
module.exports = new DescribeResidentsPage();
