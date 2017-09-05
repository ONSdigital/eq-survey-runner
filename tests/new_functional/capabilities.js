const defaultCapabilities = {
  'project': 'EQ Survey Runner',
  'tunnel-identifier': process.env.TRAVIS_JOB_NUMBER,
  'build': process.env.TRAVIS_BUILD_NUMBER,
  'public': true,
  'maxInstances': 1,
  'browserstack.local': true
};

const chrome = Object.assign({
  browserName: 'chrome'
}, defaultCapabilities);

const chromeNoJS = Object.assign(
  {
    name: 'Chrome (No JavaScript)',
    chromeOptions: {
      prefs: {'profile.managed_default_content_settings.javascript': 2}
    }
  },
  chrome
);

const chromeHeadless = Object.assign(
  {
    name: 'Chrome Headless',
    chromeOptions: {
      args: ['--headless', '--window-size=1024,1158']
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
    browserName: 'firefox',
    version: '43.0',
    platform: 'OS X 10.11'
  }, defaultCapabilities);

const edge = Object.assign(
  {
    browserName: 'microsoftedge',
    platform: 'Windows 10'
  }, defaultCapabilities);

const ie11 = Object.assign(
  {
    browserName: 'internet explorer',
    version: '11.0',
    platform: 'Windows 7'
  }, defaultCapabilities);

const ie10 = Object.assign(
  {
    browserName: 'internet explorer',
    version: '10.0',
    platform: 'Windows 7'
  }, defaultCapabilities);

const ie9 = Object.assign(
  {
    browserName: 'internet explorer',
    version: '9.0',
    platform: 'Windows 7'
  }, defaultCapabilities);

const ie8 = Object.assign(
  {
    browserName: 'internet explorer',
    version: '8.0',
    platform: 'Windows XP'
  }, defaultCapabilities);

module.exports = {
  chrome,
  chromeNoJS,
  chromeHeadless,
  phantomjs,
  firefox,
  edge,
  ie11,
  ie10,
  ie9,
  ie8
};
