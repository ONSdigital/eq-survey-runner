const helpers = require('../helpers');
const TextFieldPage = require('../generated_pages/textfield/name-block.page.js');
const SummaryPage = require('../generated_pages/textfield/summary.page.js');

describe('Textfield', function() {

  it('Given a textfield option, a user should be able to click the label of the textfield to focus', function() {
    return helpers.openQuestionnaire('test_textfield.json').then(() => {
      return browser
        .click(TextFieldPage.nameLabel())
        .hasFocus(TextFieldPage.name()).should.eventually.be.true;
      });
    });

  it('Given a text entered in textfield , When user submits and revisits the textfield, Then the textfield must contain the text entered previously', function() {
    return helpers.openQuestionnaire('test_textfield.json').then(() => {
      return browser
        .setValue(TextFieldPage.name(), "'Twenty><&Five'")
        .click(TextFieldPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.nameAnswer()).should.eventually.contain("Twenty><&Five'")
        .click(SummaryPage.nameAnswerEdit())
        .getValue(TextFieldPage.name()).should.eventually.contain("'Twenty><&Five'");
      });
    });
});
