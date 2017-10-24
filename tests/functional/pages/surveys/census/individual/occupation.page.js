// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class OccupationPage extends QuestionPage {

  constructor() {
    super('occupation');
  }

  retiredWhetherReceivingAPensionOrNot() {
    return '#occupation-answer-0';
  }

  retiredWhetherReceivingAPensionOrNotLabel() { return '#label-occupation-answer-0'; }

  aStudent() {
    return '#occupation-answer-1';
  }

  aStudentLabel() { return '#label-occupation-answer-1'; }

  lookingAfterHomeOrFamily() {
    return '#occupation-answer-2';
  }

  lookingAfterHomeOrFamilyLabel() { return '#label-occupation-answer-2'; }

  longTermSickOrDisabled() {
    return '#occupation-answer-3';
  }

  longTermSickOrDisabledLabel() { return '#label-occupation-answer-3'; }

  other() {
    return '#occupation-answer-4';
  }

  otherLabel() { return '#label-occupation-answer-4'; }

}
module.exports = new OccupationPage();
