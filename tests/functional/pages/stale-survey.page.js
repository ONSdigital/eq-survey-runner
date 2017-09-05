class StaleSurvey {

  hasStaleSurveyError() {
    return browser.isExisting('[data-qa="stale-survey-error"]')
  }

}

export default new StaleSurvey()
