const helpers = require('../helpers');
const TextFieldPage = require('../pages/surveys/textfield/block.page.js');
const MinMaxBlockPage = require('../pages/surveys/textfield/min-max-block.page');
const SummaryPage = require('../pages/surveys/textfield/summary.page.js');

describe('Textfield', function() {

  it('Given a textfield option, a user should be able to click the label of the textfield to focus', function() {
    return helpers.openQuestionnaire('test_textfield.json').then(() => {
      return browser
        .click(TextFieldPage.answerLabel())
        .hasFocus(TextFieldPage.answer()).should.eventually.be.true;
      });
    });

  it('Given a text entered in textfield , When user submits and revisits the textfield, Then the textfield must contain the text entered previously', function() {
    return helpers.openQuestionnaire('test_textfield.json').then(() => {
      return browser
        .setValue(TextFieldPage.answer(), "'Twenty><&Five'")
        .click(TextFieldPage.submit())
        // Interstitial displaying min-max formats
        .click(MinMaxBlockPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer()).should.eventually.contain("Twenty><&Five'")
        .click(SummaryPage.answerEdit())
        .getValue(TextFieldPage.answer()).should.eventually.contain("'Twenty><&Five'");
      });
    });
});
