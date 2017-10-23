// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class CompletionPreferenceIndividualPage extends QuestionPage {

  constructor() {
    super('completion-preference-individual');
  }

  online() {
    return '#completion-preference-individual-answer-0';
  }

  onlineLabel() { return '#label-completion-preference-individual-answer-0'; }

  paper() {
    return '#completion-preference-individual-answer-1';
  }

  paperLabel() { return '#label-completion-preference-individual-answer-1'; }

  notSure() {
    return '#completion-preference-individual-answer-2';
  }

  notSureLabel() { return '#label-completion-preference-individual-answer-2'; }

}
module.exports = new CompletionPreferenceIndividualPage();
