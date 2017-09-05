const helpers = require('../helpers');

describe('Feedback Form', function() {
  const schema = 'test_textfield.json';
  const formUrl = '/feedback';
  const thankyouUrlMatcher = /\/feedback\/thank-you$/;
  const submitButton = '[data-qa="btn-submit"]';
  const messageField = '#feedback-message';
  const nameField = '#feedback-name';
  const emailField = '#feedback-email';

  describe('When the form is loaded', function() {
    before('load the form', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser.url(formUrl);
        });
    });

    it('Has a message label associated with a textarea', function() {
      return browser
        .click('#feedback-message-label')
        .hasFocus(messageField).should.eventually.be.true;
    });

    it('Has a name label associated with an input', function() {
      return browser
        .click('#feedback-name-label')
        .hasFocus(nameField).should.eventually.be.true;
    });

    it('Has a email label associated with an input', function() {
      return browser
        .click('#feedback-email-label')
        .hasFocus(emailField).should.eventually.be.true;
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
          .click(submitButton)
          .getUrl().should.eventually.match(thankyouUrlMatcher);
      });
    });


    describe('and the user populates the message and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return browser
          .setValue(messageField, "This is a <script>message</script>")
          .click(submitButton)
          .getUrl().should.eventually.match(thankyouUrlMatcher);
      });
    });

    describe('and the user populates the name and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return browser
          .setValue(nameField, "This is <script>my name</script>")
          .click(submitButton)
          .getUrl().should.eventually.match(thankyouUrlMatcher);
      });
    });

    describe('and the user populates the email and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return browser
          .setValue(emailField, "This is <script>my email</script>")
          .click(submitButton)
          .getUrl().should.eventually.match(thankyouUrlMatcher);
      });
    });
  });

});
