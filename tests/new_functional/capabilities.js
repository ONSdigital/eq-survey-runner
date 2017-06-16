const defaultCapabilities = {
  'tunnel-identifier': process.env.TRAVIS_JOB_NUMBER,
  'build': process.env.TRAVIS_BUILD_NUMBER,
  'public': true,
  'maxInstances': 1
};

const chrome = Object.assign({
  name: 'Chrome 48 | OS X 10.11',
  browserName: 'chrome',
  version: '48.0',
  platform: 'OS X 10.11'
}, defaultCapabilities);

const chromeNoJS = Object.assign(
  {
    name: 'Chrome (No JavaScript) 48 | OS X 10.11',
    chromeOptions: {
      prefs: {'profile.managed_default_content_settings.javascript': 2}
    }
  },
  chrome
);

const phantomjs = {
  name: 'PhantomJS',
  browserName: 'phantomjs'
};

const firefox = Object.assign(
  {
    name: 'Firefox 43 | OS X 10.11',
    browserName: 'firefox',
    version: '43.0',
    platform: 'OS X 10.11'
  }, defaultCapabilities);

const edge = Object.assign(
  {
    name: 'MS Edge | Windows 10',
    browserName: 'microsoftedge',
    platform: 'Windows 10'
  }, defaultCapabilities);

const ie11 = Object.assign(
  {
    name: 'IE11 | Windows 7',
    browserName: 'internet explorer',
    version: '11.0',
    platform: 'Windows 7'
  }, defaultCapabilities);

const ie10 = Object.assign(
  {
    name: 'IE10 | Windows 7',
    browserName: 'internet explorer',
    version: '10.0',
    platform: 'Windows 7'
  }, defaultCapabilities);

const ie9 = Object.assign(
  {
    name: 'IE9 | Windows 7',
    browserName: 'internet explorer',
    version: '9.0',
    platform: 'Windows 7'
  }, defaultCapabilities);

const ie8 = Object.assign(
  {
    name: 'IE8 | Windows XP',
    browserName: 'internet explorer',
    version: '8.0',
    platform: 'Windows XP'
  }, defaultCapabilities);

module.exports = {
  chrome,
  chromeNoJS,
  phantomjs,
  firefox,
  edge,
  ie11,
  ie10,
  ie9,
  ie8
};
