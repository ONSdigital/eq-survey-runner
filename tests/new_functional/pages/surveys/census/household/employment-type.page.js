// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class EmploymentTypePage extends QuestionPage {

  constructor() {
    super('employment-type');
  }

  workingAsAnEmployee() {
    return '#employment-type-answer-0';
  }

  onAGovernmentSponsoredTrainingScheme() {
    return '#employment-type-answer-1';
  }

  selfEmployedOrFreelance() {
    return '#employment-type-answer-2';
  }

  workingPaidOrUnpaidForYouOwnOrYourFamilySBusiness() {
    return '#employment-type-answer-3';
  }

  awayFromWorkIllOnMaternityLeaveOnHolidayOrTemporarilyLaidOff() {
    return '#employment-type-answer-4';
  }

  doingAnyOtherKindOfPaidWork() {
    return '#employment-type-answer-5';
  }

  noneOfTheAbove() {
    return '#employment-type-answer-6';
  }

}
module.exports = new EmploymentTypePage();
