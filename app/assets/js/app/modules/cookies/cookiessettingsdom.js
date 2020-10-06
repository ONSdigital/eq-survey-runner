import domready from '../domready'
import CookiesSettings from './cookiessettings'

async function cookiesSettings() {
  const cookiesSettings = [...document.querySelectorAll('[data-module="cookie-settings"]')]
  if (cookiesSettings.length) {
    cookiesSettings.forEach(form => {
      // eslint-disable-next-line no-new
      new CookiesSettings(form)
    })
  }
}

domready(cookiesSettings)
