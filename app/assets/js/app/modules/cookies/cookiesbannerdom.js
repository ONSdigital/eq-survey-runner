import domready from '../domready'
import CookiesBanner from './cookiesbanner'

function cookiesBanner() {
  const cookiesBanner = [...document.querySelectorAll('.cookies-banner')]

  if (cookiesBanner.length) {
    cookiesBanner.forEach(banner => {
      // eslint-disable-next-line no-new
      new CookiesBanner(banner)
    })
  }
}

domready(cookiesBanner)
