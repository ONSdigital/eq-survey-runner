class ThankYou {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('thank-you') > -1
  }

}

export default new ThankYou()
