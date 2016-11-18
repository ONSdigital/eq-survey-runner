import InterstitialPage from '../../interstitial.page'

class BreakfastInterstitialPage extends InterstitialPage {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('breakfast-interstitial') > -1
  }

}

export default new BreakfastInterstitialPage()
