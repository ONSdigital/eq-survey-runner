const ConfirmAnswersBlockPage = require('../../generated_pages/placeholder_playback_list/confirm-answers-block.page');
const MandatoryCheckboxPage = require('../../generated_pages/placeholder_playback_list/mandatory-checkbox.page');

describe('Feature: Playback Confirmation', function() {

  beforeEach('Open the schema', function() {
    browser.openQuestionnaire('test_placeholder_playback_list.json');
  });

  it('When the user submits an answer, their answers should be shown on the confirmation screen', function() {
    $(MandatoryCheckboxPage.cheese()).click();
    $(MandatoryCheckboxPage.ham()).click();
    $(MandatoryCheckboxPage.submit()).click();

    expect($('body ul').getHTML()).to.contain('Cheese');
    expect($('body ul').getHTML()).to.contain('Ham');
  });
});
