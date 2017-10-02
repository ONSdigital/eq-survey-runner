// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class GeographicMarketsPage extends QuestionPage {

  constructor() {
    super('geographic-markets');
  }

  ukRegionalWithinApproximately100MilesOfThisBusiness() {
    return '#geographic-markets-answer-0';
  }

  ukRegionalWithinApproximately100MilesOfThisBusinessLabel() { return '#label-geographic-markets-answer-0'; }

  ukNational() {
    return '#geographic-markets-answer-1';
  }

  ukNationalLabel() { return '#label-geographic-markets-answer-1'; }

  europeanCountries() {
    return '#geographic-markets-answer-2';
  }

  europeanCountriesLabel() { return '#label-geographic-markets-answer-2'; }

  allOtherCountries() {
    return '#geographic-markets-answer-3';
  }

  allOtherCountriesLabel() { return '#label-geographic-markets-answer-3'; }

}
module.exports = new GeographicMarketsPage();
