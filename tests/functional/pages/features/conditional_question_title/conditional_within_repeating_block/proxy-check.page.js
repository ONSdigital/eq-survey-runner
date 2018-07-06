// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class ProxyCheckPage extends QuestionPage {

  constructor() {
    super('proxy-check');
  }

  noProxy() {
    return '#proxy-check-answer-0';
  }

  noProxyLabel() { return '#label-proxy-check-answer-0'; }

  proxy() {
    return '#proxy-check-answer-1';
  }

  proxyLabel() { return '#label-proxy-check-answer-1'; }

}
module.exports = new ProxyCheckPage();
