import domready from '../domready'
import CookiesBanner from './cookiesbanner'

function cookiesBanner() {
  const cookiesBanner = [...document.querySelectorAll('.cookies-banner')]

  if (cookiesBanner.length) {
    alert('I am existing an in here')
    cookiesBanner.forEach(banner => {
      // eslint-disable-next-line no-new
      new CookiesBanner(banner)
    })
    alert('made it this far')
  }
}

domready(cookiesBanner)
