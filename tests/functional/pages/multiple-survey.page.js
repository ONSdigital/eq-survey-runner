class MultipleSurveys {

  hasMultipleSurveyError() {
    return browser.isExisting('[data-qa="multiple-survey-error"]')
  }

}

export default new MultipleSurveys()
