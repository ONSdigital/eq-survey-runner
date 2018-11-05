const helpers = require('../helpers');
const form = require('../base_pages/feedback-form');

describe('Feedback Form', function() {
  const schema = 'test_textfield.json';
  const formUrl = '/feedback';
  const thankyouUrlMatcher = /\/feedback\/thank-you$/;

  describe('When the form is loaded', function() {
    before('load the form', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser.url(formUrl);
        });
    });

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
  });

  describe('When the form is empty', function() {
    beforeEach('load the form', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser.url(formUrl);
        });
    });

    describe('and the submit button is clicked', function() {
      it('redirects to the thankyou page', function() {
        return browser
          .click(form.submit())
          .getUrl().should.eventually.match(thankyouUrlMatcher);
      });
    });


    describe('and the user populates the message and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return browser
          .setValue(form.messageInput(), "This is a <script>message</script>")
          .click(form.submit())
          .getUrl().should.eventually.match(thankyouUrlMatcher);
      });
    });

    describe('and the user populates the name and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return browser
          .setValue(form.nameInput(), "This is <script>my name</script>")
          .click(form.submit())
          .getUrl().should.eventually.match(thankyouUrlMatcher);
      });
    });

    describe('and the user populates the email and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return browser
          .setValue(form.emailInput(), "This is <script>my email</script>")
          .click(form.submit())
          .getUrl().should.eventually.match(thankyouUrlMatcher);
      });
    });
  });

});
