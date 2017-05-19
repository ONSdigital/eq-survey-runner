// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class SelfContainedAccommodationPage extends QuestionPage {

  constructor() {
    super('self-contained-accommodation');
  }

  yesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse() {
    return '#self-contained-accommodation-answer-0';
  }

  no() {
    return '#self-contained-accommodation-answer-1';
  }

}
module.exports = new SelfContainedAccommodationPage();
