const defaultCapabilities = {
  'tunnel-identifier': process.env.TRAVIS_JOB_NUMBER,
  'build': process.env.TRAVIS_BUILD_NUMBER,
  'public': true,
  'maxInstances': 1
}

export const chrome = {
  name: 'Chrome 48 | OS X 10.11',
  browserName: 'chrome',
  version: '48.0',
  platform: 'OS X 10.11',
  ...defaultCapabilities
}

export const chromeNoJS = {
  ...chrome,
  name: 'Chrome (No JavaScript) 48 | OS X 10.11',
  chromeOptions: {
    prefs: {'profile.managed_default_content_settings.javascript': 2}
  }
}

export const phantomjs = {
  name: 'PhantomJS',
  browserName: 'phantomjs'
}

export const firefox = {
  name: 'Firefox 43 | OS X 10.11',
  browserName: 'firefox',
  version: '43.0',
  platform: 'OS X 10.11',
  ...defaultCapabilities
}

export const edge = {
  name: 'MS Edge | Windows 10',
  browserName: 'microsoftedge',
  platform: 'Windows 10',
  ...defaultCapabilities
}

export const ie11 = {
  name: 'IE11 | Windows 7',
  browserName: 'internet explorer',
  version: '11.0',
  platform: 'Windows 7',
  ...defaultCapabilities
}

export const ie10 = {
  name: 'IE10 | Windows 7',
  browserName: 'internet explorer',
  version: '10.0',
  platform: 'Windows 7',
  ...defaultCapabilities
}

export const ie9 = {
  name: 'IE9 | Windows 7',
  browserName: 'internet explorer',
  version: '9.0',
  platform: 'Windows 7',
  ...defaultCapabilities
}

export const ie8 = {
  name: 'IE8 | Windows XP',
  browserName: 'internet explorer',
  version: '8.0',
  platform: 'Windows XP',
  ...defaultCapabilities
}
