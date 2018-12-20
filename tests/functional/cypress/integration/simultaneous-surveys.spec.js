import {openQuestionnaire} from '../helpers/helpers.js'
const TextFieldPage = require('../../generated_pages/textfield/name-block.page');
const TextAreaPage = require('../../generated_pages/textarea/textarea-block.page.js');
const TextAreaSummaryPage = require('../../generated_pages/textarea/textarea-summary.page.js');

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
          .switchTab(this.firstTab)
      .refresh()
      .get('[data-qa="multiple-survey-error"]').should('exist');
  });

  it('Displays a session expired error when the first tabs form is submitted (CSRF Error)', function() {
          .switchTab(this.firstTab)
      .get(TextFieldPage.submit()).click()
      .get('[data-qa="session-expired-error"]').should('exist');
  });

  it('Re-displays the textarea when the second survey is refreshed (i.e. on a GET)', function() {
          .refresh()
      .get('textarea').should('exist');
  });

  it('Displays the summary page when the second surveys form is submitted', function() {
          .get(TextAreaPage.submit()).click()
      .get(TextAreaSummaryPage.answer()).should('exist');
  });

});
