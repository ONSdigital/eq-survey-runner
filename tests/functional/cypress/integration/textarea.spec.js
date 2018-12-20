import {openQuestionnaire} from '../helpers/helpers.js'
const TextareaBlock = require('../../generated_pages/textarea/textarea-block.page.js');
const TextareaSummary = require('../../generated_pages/textarea/textarea-summary.page.js');

describe('Textarea', function() {

  const textarea_schema = 'test_textarea.json';
  const textarea_limit = '[data-qa="textarea-with-limit"]';

  it('Given a textarea option, a user should be able to click the label of the textarea to focus', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
                  .get(TextareaBlock.answerLabel()).click()
          .focused().should('match', TextareaBlock.answer())
      });
  });

  it('Given a textarea option, When no text is entered, Then the summary should display "No answer provided"', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
                  .get(TextareaBlock.submit()).click()
          .get(TextareaSummary.answer()).stripText().should('contain', 'No answer provided');
      });
  });

  it('Given a textarea option, When some text is entered, Then the summary should display the text', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
                  .get(TextareaBlock.answer()).type('Some text')
          .get(TextareaBlock.submit()).click()
          .get(TextareaSummary.answer()).stripText().should('contain', 'Some text');
      });

  });

  it('Given a text entered in textarea , When user submits and revisits the textarea, Then the textarea must contain the text entered previously', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
                  .get(TextareaBlock.answer()).type("'Twenty><&Five'")
          .get(TextareaBlock.submit()).click()
          .get(TextareaSummary.answer()).stripText().should('contain', "'Twenty><&Five'")
          .get(TextareaSummary.answerEdit()).click()
          .getValue(TextareaBlock.answer()).should.eventually.contain("'Twenty><&Five'");
      });
  });

  it('Displays the number of characters remaining', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
                  .get(textarea_limit).stripText().should('contain', '20');
      });
  });

  it('Updates the number of characters remaining when the user adds content', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
                  .get(TextareaBlock.answer()).type('Banjo')
          .get(textarea_limit).stripText().should('contain', '15');
      });
  });

  it('The user is unable to add more characters when the limit is reached', function() {
    return helpers.openQuestionnaire(textarea_schema)
      .then(() => {
                  .get(TextareaBlock.answer()).type('This sentence is over twenty characters long')
          .get(textarea_limit).stripText().should('contain', '0')
          .getValue(TextareaBlock.answer()).should.eventually.equal('This sentence is ove');
      });
  });


});
