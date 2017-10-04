const helpers = require('../helpers');
const form = require('../pages/feedback-form');

const schema = 'test_textfield.json';
const formUrl = '/feedback';
const thankyouUrlMatcher = /\/feedback\/thank-you$/;

describe('Feedback Form', function() {

  describe('When the form is loaded', function() {

    it('Has a message label associated with a textarea', function() {
      return openFeedback().then(function () {
        browser.click(form.messageLabel())
          .hasFocus(form.messageInput()).should.eventually.be.true;
      });
    });

    it('Has a name label associated with an input', function() {
      return openFeedback().then(function () {
        browser.click(form.nameLabel())
          .hasFocus(form.nameInput()).should.eventually.be.true;
      });
    });

    it('Has a email label associated with an input', function() {
      return openFeedback().then(function () {
        browser.click(form.emailLabel())
          .hasFocus(form.emailInput()).should.eventually.be.true;
      });
    });
  });

  describe('When the form is empty', function() {

    describe('and the submit button is clicked', function() {
      it('redirects to the thankyou page', function() {
        return openFeedback().then(function () {
          browser.click(form.submit())
            .getUrl().should.eventually.match(thankyouUrlMatcher);
        });
      });
    });


    describe('and the user populates the message and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return openFeedback().then(function () {
          browser.setValue(form.messageInput(), "This is a <script>message</script>")
            .click(form.submit())
            .getUrl().should.eventually.match(thankyouUrlMatcher);
        });
      });
    });

    describe('and the user populates the name and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return openFeedback().then(function () {
          browser.setValue(form.nameInput(), "This is <script>my name</script>")
            .click(form.submit())
            .getUrl().should.eventually.match(thankyouUrlMatcher);
        });
      });
    });

    describe('and the user populates the email and clicks submit', function() {
      it('redirects to the thankyou page', function() {
        return openFeedback().then(function () {
          browser.setValue(form.emailInput(), "This is <script>my email</script>")
            .click(form.submit())
            .getUrl().should.eventually.match(thankyouUrlMatcher);
        });
      });
    });
  });

});

function openFeedback() {
  return helpers.openQuestionnaire(schema)
        .then(function() {
          return browser.url(formUrl);
        });
}
