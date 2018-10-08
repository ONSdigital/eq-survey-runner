// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusivePercentagePage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-percentage');
  }

  percentage() {
    return '#percentage-answer';
  }

  percentageLabel() { return '#label-percentage-answer'; }

  percentageExclusiveIPreferNotToSay() {
    return '#percentage-exclusive-answer-0';
  }

  percentageExclusiveIPreferNotToSayLabel() { return '#label-percentage-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusivePercentagePage();
