const helpers = require('../helpers');
const TextFieldPage = require('../pages/surveys/textfield/block.page.js');

describe('Textfield', function() {

  it('Given a textfield option, a user should be able to click the label of the textfield to focus', function() {
    return helpers.openQuestionnaire('test_textfield.json').then(() => {
      return browser
        .click(TextFieldPage.answerLabel())
        .hasFocus(TextFieldPage.answer()).should.eventually.be.true;
      });
    });
});
