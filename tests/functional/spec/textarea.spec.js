const helpers = require('../helpers');
const TextareaBlock = require('../generated_pages/textarea/textarea-block.page.js');
const TextareaSummary = require('../generated_pages/textarea/textarea-summary.page.js');

describe('Textarea', function() {

  const textarea_schema = 'test_textarea.json';
  const textarea_limit = `${TextareaBlock.answer()} + [data-charcount-singular]`;

  it('Given a textarea option, a user should be able to click the label of the textarea to focus', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
        return browser
          .click(TextareaBlock.answerLabel())
          .hasFocus(TextareaBlock.answer()).should.eventually.be.true;
      });
  });

  it('Given a textarea option, When no text is entered, Then the summary should display "No answer provided"', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
        return browser
          .click(TextareaBlock.submit())
          .getText(TextareaSummary.answer()).should.eventually.contain('No answer provided');
      });
  });

  it('Given a textarea option, When some text is entered, Then the summary should display the text', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
        return browser
          .setValue(TextareaBlock.answer(), 'Some text')
          .click(TextareaBlock.submit())
          .getText(TextareaSummary.answer()).should.eventually.contain('Some text');
      });

  });

  it('Given a text entered in textarea , When user submits and revisits the textarea, Then the textarea must contain the text entered previously', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
        return browser
          .setValue(TextareaBlock.answer(), "'Twenty><&Five'")
          .click(TextareaBlock.submit())
          .getText(TextareaSummary.answer()).should.eventually.contain("'Twenty><&Five'")
          .click(TextareaSummary.answerEdit())
          .getValue(TextareaBlock.answer()).should.eventually.contain("'Twenty><&Five'");
      });
  });

  it('Displays the number of characters remaining', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
        return browser
          .getText(textarea_limit).should.eventually.contain('20');
      });
  });

  it('Updates the number of characters remaining when the user adds content', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
        return browser
          .setValue(TextareaBlock.answer(), 'Banjo')
          .getText(textarea_limit).should.eventually.contain('15');
      });
  });

  it('The user is unable to add more characters when the limit is reached', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
        return browser
          .setValue(TextareaBlock.answer(), 'This sentence is over twenty characters long')
          .getText(textarea_limit).should.eventually.contain('0')
          .getValue(TextareaBlock.answer()).should.eventually.equal('This sentence is ove');
      });
  });


});
