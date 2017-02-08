// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class GeographicMarketsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('geographic-markets')
  }

  clickGeographicMarketsAnswerUkRegionalWithinApproximately100MilesOfThisBusiness() {
    browser.element('[id="geographic-markets-answer-0"]').click()
    return this
  }

  clickGeographicMarketsAnswerUkNational() {
    browser.element('[id="geographic-markets-answer-1"]').click()
    return this
  }

  clickGeographicMarketsAnswerEuropeanCountries() {
    browser.element('[id="geographic-markets-answer-2"]').click()
    return this
  }

  clickGeographicMarketsAnswerAllOtherCountries() {
    browser.element('[id="geographic-markets-answer-3"]').click()
    return this
  }

}

export default new GeographicMarketsPage()
