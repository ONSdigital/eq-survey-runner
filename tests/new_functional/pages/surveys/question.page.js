const BasePage = require('../base.page');

class QuestionPage extends BasePage {

  constructor(pageName) {
    super(pageName);
    this.questions = [];
  }

  alert() { return '[data-qa="error-body"]';  }

  error() { return '.js-inpagelink'; }

  previous() { return 'a[id="top-previous"]'; }

  displayedName() { return '[data-qa="section-title"]'; }

  submit() { return '[data-qa="btn-submit"]'; }


}

module.exports = QuestionPage;
