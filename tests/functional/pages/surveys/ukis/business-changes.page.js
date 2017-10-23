// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class BusinessChangesPage extends QuestionPage {

  constructor() {
    super('business-changes');
  }

  businessPracticesYes() {
    return '#business-changes-business-practices-answer-0';
  }

  businessPracticesYesLabel() { return '#label-business-changes-business-practices-answer-0'; }

  businessPracticesNo() {
    return '#business-changes-business-practices-answer-1';
  }

  businessPracticesNoLabel() { return '#label-business-changes-business-practices-answer-1'; }

  organisingYes() {
    return '#business-changes-organising-answer-0';
  }

  organisingYesLabel() { return '#label-business-changes-organising-answer-0'; }

  organisingNo() {
    return '#business-changes-organising-answer-1';
  }

  organisingNoLabel() { return '#label-business-changes-organising-answer-1'; }

  externalRelationshipsYes() {
    return '#business-changes-external-relationships-answer-0';
  }

  externalRelationshipsYesLabel() { return '#label-business-changes-external-relationships-answer-0'; }

  externalRelationshipsNo() {
    return '#business-changes-external-relationships-answer-1';
  }

  externalRelationshipsNoLabel() { return '#label-business-changes-external-relationships-answer-1'; }

  yes() {
    return '#business-changes-answer-0';
  }

  yesLabel() { return '#label-business-changes-answer-0'; }

  no() {
    return '#business-changes-answer-1';
  }

  noLabel() { return '#label-business-changes-answer-1'; }

}
module.exports = new BusinessChangesPage();
