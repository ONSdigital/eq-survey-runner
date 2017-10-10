// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class MainJobTypePage extends QuestionPage {

  constructor() {
    super('main-job-type');
  }

  employedByAnOrganisationOrBusiness() {
    return '#main-job-type-answer-0';
  }

  employedByAnOrganisationOrBusinessLabel() { return '#label-main-job-type-answer-0'; }

  selfEmployedInYourOwnOrganisationOrBusiness() {
    return '#main-job-type-answer-1';
  }

  selfEmployedInYourOwnOrganisationOrBusinessLabel() { return '#label-main-job-type-answer-1'; }

  notWorkingForAnOrganisationOrBusiness() {
    return '#main-job-type-answer-2';
  }

  notWorkingForAnOrganisationOrBusinessLabel() { return '#label-main-job-type-answer-2'; }

}
module.exports = new MainJobTypePage();
