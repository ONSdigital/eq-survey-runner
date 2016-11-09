class MultipleSurveys {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('multiple-surveys') > -1
  }

}

export default new MultipleSurveys()
