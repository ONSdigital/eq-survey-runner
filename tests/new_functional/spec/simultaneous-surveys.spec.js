const helpers = require('../helpers');
const TextFieldPage = require('../pages/surveys/textfield/block.page.js');
const TextAreaPage = require('../pages/surveys/textarea/textarea-block.page.js');
const TextAreaSummaryPage = require('../pages/surveys/textarea/textarea-summary.page.js');

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
        .setViewportSize({ width: 1024, height: 1158 })
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

  it('Displays a multiple survey error when the first tabs form is submitted', function() {
    return browser
      .switchTab(this.firstTab)
      .click(TextFieldPage.submit())
      .isExisting('[data-qa="multiple-survey-error"]').should.eventually.be.true;
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
