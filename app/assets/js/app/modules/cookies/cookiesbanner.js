import { cookie, setDefaultConsentCookie, approveAllCookieTypes, setConsentCookie, parseCookie } from './cookiesfunctions'

export default class CookiesBanner {
  constructor(component) {
    this.component = component
    this.primaryBanner = this.component.querySelector('.cookies-banner__primary')
    this.confirmBanner = this.component.querySelector('.cookies-banner__confirmation')
    this.button = this.component.querySelector('.js-accept-cookies')
    this.hideButton = this.component.querySelector('.js-hide-button')

    this.setupCookiesEvents()
  }

  setupCookiesEvents() {
    this.button.addEventListener('click', this.setCookiesConsent.bind(this))
    this.hideButton.addEventListener('click', this.hideConfirmBanner.bind(this))
    this.showCookiesMessage()
  }

  showCookiesMessage() {
    const displayCookiesBanner = this.component && cookie('ons_cookie_message_displayed') !== 'true'
    let policy = cookie('ons_cookie_policy')
    if (policy) {
      setConsentCookie(parseCookie(policy))
    }
    if (displayCookiesBanner) {
      this.component.style.display = 'block'

      if (!cookie('ons_cookie_policy')) {
        setDefaultConsentCookie()
      }
    }
  }

  setCookiesConsent(event) {
    event.preventDefault()
    approveAllCookieTypes()
    cookie('ons_cookie_message_displayed', 'true', { days: 365 })
    this.hidePrimaryCookiesBanner()
  }

  hidePrimaryCookiesBanner() {
    if (this.component) {
      this.primaryBanner.style.display = 'none'
      this.confirmBanner.classList.remove('u-d-no')
      this.confirmBanner.setAttribute('aria-live', 'polite')
      this.confirmBanner.setAttribute('role', 'status')
    }
  }

  hideConfirmBanner() {
    if (this.component) {
      this.component.style.display = 'none'
    }
  }
}
