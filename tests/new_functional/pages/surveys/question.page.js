const BasePage = require('../base.page');

class QuestionPage extends BasePage {

  constructor(pageName) {
    super(pageName);
    this.questions = [];
  }

  alert() { return '[data-qa="error-body"]';  }

  error() { return '.js-inpagelink'; }

  errorNumber(number) { return 'ul > li:nth-child(' + number + ') > a'; }

  previous() { return 'a[id="top-previous"]'; }

  displayedName() { return '[data-qa="block-title"]'; }

  submit() { return '[data-qa="btn-submit"]'; }


}

module.exports = QuestionPage;
