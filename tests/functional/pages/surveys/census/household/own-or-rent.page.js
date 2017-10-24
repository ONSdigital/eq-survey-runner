// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class OwnOrRentPage extends QuestionPage {

  constructor() {
    super('own-or-rent');
  }

  ownsOutright() {
    return '#own-or-rent-answer-0';
  }

  ownsWithAMortgageOrLoan() {
    return '#own-or-rent-answer-1';
  }

  partOwnsAndPartRentsSharedOwnership() {
    return '#own-or-rent-answer-2';
  }

  rentsWithOrWithoutHousingBenefit() {
    return '#own-or-rent-answer-3';
  }

  livesHereRentFree() {
    return '#own-or-rent-answer-4';
  }

}
module.exports = new OwnOrRentPage();
