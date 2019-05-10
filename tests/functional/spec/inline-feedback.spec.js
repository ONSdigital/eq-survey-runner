const helpers = require('../helpers');
const form = require('../base_pages/feedback-form.js');

describe('Inline Feedback Form', function() {
  const schema = 'test_textfield.json';

  describe('When the survey is loaded', function() {
    before('load the form', function() {
      return helpers.openQuestionnaire(schema);
    });

    it('the form is not visible', theFormIsNotVisible);

    describe('and the open action is clicked', function() {
      before('click the open action', function() {
        return browser.click(form.open());
      });

      it('the form is visible', theFormIsVisible);

      it('Has a message label associated with a textarea', function() {
        return browser
          .click(form.messageLabel())
          .hasFocus(form.messageInput()).should.eventually.be.true;
      });

      it('Has a name label associated with an input', function() {
        return browser
          .click(form.nameLabel())
          .hasFocus(form.nameInput()).should.eventually.be.true;
      });

      it('Has a email label associated with an input', function() {
        return browser
          .click(form.emailLabel())
          .hasFocus(form.emailInput()).should.eventually.be.true;
      });

      it('Has a cancel link', function() {
        return browser
          .isVisible(form.close()).should.eventually.be.true;
      });

      describe('and the close action is clicked', function() {
        before('click the close action', function() {
          return browser.click(form.close());
        });

        it('the form is not visible', theFormIsNotVisible);
      });

    });
  });

  describe('When the form is empty', function() {
    const goodSubmitBehaviour = 'the form is not visible and the thanks container is displayed';

    beforeEach('load and display the form', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
            .click(form.open());
        });
    });

    it(`and the user populates the message ${goodSubmitBehaviour}`, function() {
      return browser
        .waitForVisible(form.messageInput())
        .setValue(form.messageInput(), "This is <script>my name</script>")
        .click(form.submit())
        .then(theFormIsNotVisibleWithThanks);
    });


    it(`and the user populates the name ${goodSubmitBehaviour}`, function() {
      return browser
        .waitForVisible(form.nameInput())
        .setValue(form.nameInput(), "This is <script>my name</script>")
        .click(form.submit())
        .then(theFormIsNotVisibleWithThanks);
    });

    it(`and the user populates the email ${goodSubmitBehaviour}`, function() {
      return browser
        .waitForVisible(form.emailInput())
        .setValue(form.emailInput(), "This is <script>my email</script>")
        .click(form.submit())
        .then(theFormIsNotVisibleWithThanks);
    });

  });

  function theFormIsNotVisibleWithThanks() {
    const withThanks = true;
    return theFormIsNotVisible(withThanks);
  }

  function theFormIsNotVisible(withThanks=false ) {
    let chain = browser.waitForVisible(form.container(), 2000, true).should.eventually.be.true;

    if (withThanks) {
      return chain
        .isExisting(form.display()).should.eventually.be.false
        .isVisible(form.thanks()).should.eventually.be.true;
    }

    return chain
      .isExisting(form.display()).should.eventually.be.true
      .isVisible(form.thanks()).should.eventually.be.false;
  }

  function theFormIsVisible() {
    // Animation so wait for visible
    return browser
      .waitForVisible(form.container()).should.eventually.be.true
      .isVisible(form.display()).should.eventually.be.true
      .isVisible(form.thanks()).should.eventually.be.false;
  }
});
