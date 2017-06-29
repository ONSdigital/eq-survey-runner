const defaultCapabilities = {
  'project': 'EQ Survey Runner',
  'tunnel-identifier': process.env.TRAVIS_JOB_NUMBER,
  'build': process.env.TRAVIS_BUILD_NUMBER,
  'public': true,
  'maxInstances': 1,
  'browserstack.local': true
}

export const chrome = {
  browserName: 'chrome',
  browser_version: '48.0',
  os: 'OS X',
  os_version: 'Yosemite',
  ...defaultCapabilities
}

export const chromeNoJS = {
  ...chrome,
  name: 'Chrome (No JavaScript)',
  chromeOptions: {
    prefs: {'profile.managed_default_content_settings.javascript': 2}
  }
}

export const phantomjs = {
  name: 'PhantomJS',
  browserName: 'phantomjs'
}

export const firefox = {
  browserName: 'firefox',
  version: '43.0',
  os: 'OS X',
  ...defaultCapabilities
}

export const edge = {
  browserName: 'microsoftedge',
  os: 'Windows',
  os_version: '10',
  ...defaultCapabilities
}

export const ie11 = {
  browserName: 'internet explorer',
  version: '11.0',
  os: 'Windows',
  os_version: '7',
  ...defaultCapabilities
}

export const ie10 = {
  browserName: 'internet explorer',
  version: '10.0',
  os: 'Windows',
  os_version: '7',
  ...defaultCapabilities
}

export const ie9 = {
  browserName: 'internet explorer',
  version: '9.0',
  os: 'Windows',
  os_version: '7',
  ...defaultCapabilities
}

export const ie8 = {
  browserName: 'internet explorer',
  version: '8.0',
  os: 'Windows',
  os_version: 'XP',
  ...defaultCapabilities
}
