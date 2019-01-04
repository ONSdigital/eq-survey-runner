import {openQuestionnaire} from '../helpers/helpers.js';
const form = require('../../base_pages/feedback-form.js');

describe('Inline Feedback Form', function() {
  const schema = 'test_textfield.json';

  describe('When the survey is loaded', function() {
    beforeEach('load the form', function() {
      return openQuestionnaire(schema);
    });

    it('the form is not visible', theFormIsNotVisible);

    describe('and the open action is clicked', function() {
      beforeEach('click the open action', function() {
        cy.get(form.open()).click();
      });

      it('the form is visible', theFormIsVisible);

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

      it('Has a cancel link', function() {
        cy
          .get(form.close()).should('be.visible');
      });

      describe('and the close action is clicked', function() {
        before('click the close action', function() {
          return cy.get(form.close()).click();
        });

        it('the form is not visible', theFormIsNotVisible);
      });

    });
  });

  describe('When the form is empty', function() {
    const goodSubmitBehaviour = 'the form is not visible and the thanks container is displayed';

    beforeEach('load and display the form', function() {
      return openQuestionnaire(schema)
        .then(() => {
          cy.get(form.open()).click();
        });
    });

    it(`and the user populates the message ${goodSubmitBehaviour}`, function() {
      cy
        .get(form.messageInput())
        .get(form.messageInput()).type('This is <script>my name</script>')
        .get(form.submit()).click()
        .then(theFormIsNotVisibleWithThanks);
    });


    it(`and the user populates the name ${goodSubmitBehaviour}`, function() {
      cy
        .get(form.nameInput()).should('be.visible')
        .get(form.nameInput()).type('This is <script>my name</script>')
        .get(form.submit()).click()
        .then(theFormIsNotVisibleWithThanks);
    });

    it(`and the user populates the email ${goodSubmitBehaviour}`, function() {
      cy
        .get(form.emailInput()).should('be.visible')
        .get(form.emailInput()).type('This is <script>my email</script>')
        .get(form.submit()).click()
        .then(theFormIsNotVisibleWithThanks);
    });

  });

  function theFormIsNotVisibleWithThanks() {
    const withThanks = true;
    return theFormIsNotVisible(withThanks);
  }

  function theFormIsNotVisible(withThanks=false ) {
    let chain = cy.get(form.container());

    if (withThanks) {
      return chain
        .get(form.display()).should('not.be.visible')
        .get(form.thanks()).should('be.visible');
    }

    return chain
      .get(form.display()).should('be.visible')
      .get(form.thanks()).should('not.be.visible');
  }

  function theFormIsVisible() {
    // Animation so wait for visible
    cy
      .get(form.container()).should('be.visible')
      .get(form.display()).should('be.visible')
      .get(form.thanks()).should('not.be.visible');
  }

});
