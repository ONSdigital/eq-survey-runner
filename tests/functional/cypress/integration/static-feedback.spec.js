import {openQuestionnaire} from '../helpers/helpers.js'
const form = require('../../base_pages/feedback-form');

describe('Feedback Form', function() {
  const schema = 'test_textfield.json';
  const formUrl = '/feedback';
  const thankyouUrlMatcher = /\/feedback\/thank-you$/;

  describe('When the form is loaded', function() {
    before('load the form', function() {
      openQuestionnaire(schema)
        .then(() => {
          cy.visit(formUrl);
        });
    });

    it('Has a message label associated with a textarea', function() {
      cy
        .get(form.messageLabel()).click()
        .focused().should('match', form.messageInput());
    });

    it('Has a name label associated with an input', function() {
      cy
        .get(form.nameLabel()).click()
        .focused().should('match', form.nameInput());
    });

    it('Has a email label associated with an input', function() {
      cy
        .get(form.emailLabel()).click()
        .focused().should('match', form.emailInput());
    });
  });

  describe('When the form is empty', function() {
    beforeEach('load the form', function() {
      openQuestionnaire(schema)
        .then(() => {
          cy.visit(formUrl);
        });
    });

    describe('and the submit button is clicked', function() {
      it('redirects to the thankyou page', function() {
        cy
          .get(form.submit()).click()
          .url().should('match', thankyouUrlMatcher);
      });
    });


    describe('and the user populates the message and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        cy
          .get(form.messageInput()).type("This is a <script>message</script>")
          .get(form.submit()).click()
          .url().should('match', thankyouUrlMatcher);
      });
    });

    describe('and the user populates the name and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        cy
          .get(form.nameInput()).type("This is <script>my name</script>")
          .get(form.submit()).click()
          .url().should('match', thankyouUrlMatcher);
      });
    });

    describe('and the user populates the email and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        cy
          .get(form.emailInput()).type("This is <script>my email</script>")
          .get(form.submit()).click()
          .url().should('match', thankyouUrlMatcher);
      });
    });
  });

});
