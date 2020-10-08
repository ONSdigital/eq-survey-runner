const helpers = require('../helpers');

const cookieMessage = "ons_cookie_message_displayed";
const cookiePolicy = "ons_cookie_policy";

describe('Setting cookies', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('0_star_wars.json');
  });

  afterEach(function() {
    return browser.deleteCookie();
  });

  it('Given the accept all cookies button is pressed then the hide button should be revealed and cookies set', function() {
    return browser
      // When
      .waitForExist('.js-accept-cookies')
      .click('.js-accept-cookies')
      // Then
      .waitForExist('.js-hide-button')
      .getCookie(cookieMessage).then(item => item.value).should.eventually.equal('true')
      .getCookie(cookiePolicy).then(item => item.value).should.eventually.equal('{"essential":true,"usage":true}');
  });

  it('Given the "ons_cookie_message_display" is set when I land on a page then the cookie banner should not be present', function() {
    return browser
      // When
      .setCookie({ name: cookieMessage, value: 'true' })
      .waitForExist('.js-accept-cookies')
      .click('.js-accept-cookies')
      .refresh()
      // Then
      .waitForExist('#main')
      .isExisting('.cookies-banner').should.eventually.not.be.true;
      // doesn't exist
  });
  
  it('Given the "Set cookie preferences" button is clicked then I should be redirected', function() {
    return browser
      // When
      .waitForExist('.js-accept-cookies')
      .click('[href="/cookies-settings"]')
      // Then
      .getUrl().should.eventually.contain('cookies-settings');
  });

});

describe('Cookie settings page', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('0_star_wars.json');
  });

  afterEach(function() {
    return browser.deleteCookie();
  });

  it('Given I am on the cookies-settings page when I accept specific cookies then they are set in my browser', function() {
    return browser
      // When
      .waitForExist('.js-accept-cookies')
      .click('[href="/cookies-settings"]')
      .waitForExist('#on-1')
      .getCookie(cookiePolicy).then(item => item.value).should.eventually.equal('{"essential":true,"usage":false}')
      .click('#on-1')
      .click('.cookies-submit-btn')
      // Then
      .getCookie(cookiePolicy).then(item => item.value).should.eventually.equal('{"essential":true,"usage":true}');
  });

  it('Given I am on the cookies-settings page when I reject specific cookies then they are set in my browser', function() {
    return browser
    // When
    .setCookie({ name: cookiePolicy, value: '{"essential":true,"usage":true}' })
    .waitForExist('.js-accept-cookies')
    .click('[href="/cookies-settings"]')
    .waitForExist('#off-1')
    .click('#off-1')
    .click('.cookies-submit-btn')
    .refresh()
    // Then
    .getCookie(cookiePolicy).then(item => item.value).should.eventually.equal('{"essential":true,"usage":false}');
  });

});