// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class CentralHeatingPage extends QuestionPage {

  constructor() {
    super('central-heating');
  }

  noCentralHeating() {
    return '#central-heating-answer-0';
  }

  gas() {
    return '#central-heating-answer-1';
  }

  electricIncludingStorageHeaters() {
    return '#central-heating-answer-2';
  }

  oil() {
    return '#central-heating-answer-3';
  }

  solidFuelForExampleWoodCoal() {
    return '#central-heating-answer-4';
  }

  otherCentralHeating() {
    return '#central-heating-answer-5';
  }

}
module.exports = new CentralHeatingPage();
