// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SkipInterstitialPage extends QuestionPage {

  constructor() {
    super('skip-interstitial');
  }

  yes() {
    return '#skip-interstitial-answer-0';
  }

  yesLabel() { return '#label-skip-interstitial-answer-0'; }

  no() {
    return '#skip-interstitial-answer-1';
  }

  noLabel() { return '#label-skip-interstitial-answer-1'; }

}
module.exports = new SkipInterstitialPage();
