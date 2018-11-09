const helpers = require('../helpers');
const TextFieldPage = require('../generated_pages/textfield/name-block.page');
const TextAreaPage = require('../generated_pages/textarea/textarea-block.page.js');
const TextAreaSummaryPage = require('../generated_pages/textarea/textarea-summary.page.js');

describe('Given the user launches two surveys', function() {
  beforeEach('Launch two surveys', function() {
    this.secondTab = 'secondTab';

    let launchFirstTab = helpers.openQuestionnaire('test_textfield.json')
        .then( () => {
          return browser.getCurrentTabId();
        })
        .then( (tabId) => {
          return this.firstTab = tabId;
        });

    let launchSecondTab = browser
        .newWindow('/status', this.secondTab)
        .then( () => {
          return helpers.openQuestionnaire('test_textarea.json');
        });

    return Promise.all([launchFirstTab, launchSecondTab]);

  });

  it('Displays a multiple survey error when the first survey is refreshed (i.e. on a GET)', function() {
    return browser
      .switchTab(this.firstTab)
      .refresh()
      .isExisting('[data-qa="multiple-survey-error"]').should.eventually.be.true;
  });

  it('Displays a session expired error when the first tabs form is submitted (CSRF Error)', function() {
    return browser
      .switchTab(this.firstTab)
      .click(TextFieldPage.submit())
      .isExisting('[data-qa="session-expired-error"]').should.eventually.be.true;
  });

  it('Re-displays the textarea when the second survey is refreshed (i.e. on a GET)', function() {
    return browser
      .refresh()
      .isExisting('textarea').should.eventually.be.true;
  });

  it('Displays the summary page when the second surveys form is submitted', function() {
    return browser
      .click(TextAreaPage.submit())
      .isExisting(TextAreaSummaryPage.answer()).should.eventually.be.true;
  });

});
