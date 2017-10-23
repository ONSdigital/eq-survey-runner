// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class PublicFinancialSupportPage extends QuestionPage {

  constructor() {
    super('public-financial-support');
  }

  authoritiesYes() {
    return '#public-financial-support-authorities-answer-0';
  }

  authoritiesYesLabel() { return '#label-public-financial-support-authorities-answer-0'; }

  authoritiesNo() {
    return '#public-financial-support-authorities-answer-1';
  }

  authoritiesNoLabel() { return '#label-public-financial-support-authorities-answer-1'; }

  centralGovernmentYes() {
    return '#public-financial-support-central-government-answer-0';
  }

  centralGovernmentYesLabel() { return '#label-public-financial-support-central-government-answer-0'; }

  centralGovernmentNo() {
    return '#public-financial-support-central-government-answer-1';
  }

  centralGovernmentNoLabel() { return '#label-public-financial-support-central-government-answer-1'; }

  euYes() {
    return '#public-financial-support-eu-answer-0';
  }

  euYesLabel() { return '#label-public-financial-support-eu-answer-0'; }

  euNo() {
    return '#public-financial-support-eu-answer-1';
  }

  euNoLabel() { return '#label-public-financial-support-eu-answer-1'; }

}
module.exports = new PublicFinancialSupportPage();
