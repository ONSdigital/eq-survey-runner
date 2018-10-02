// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  centimetres(index = 0) { return '#centimetres-' + index + '-answer'; }

  centimetresEdit(index = 0) { return '[data-qa="centimetres-' + index + '-edit"]'; }

  metres(index = 0) { return '#metres-' + index + '-answer'; }

  metresEdit(index = 0) { return '[data-qa="metres-' + index + '-edit"]'; }

  kilometres(index = 0) { return '#kilometres-' + index + '-answer'; }

  kilometresEdit(index = 0) { return '[data-qa="kilometres-' + index + '-edit"]'; }

  miles(index = 0) { return '#miles-' + index + '-answer'; }

  milesEdit(index = 0) { return '[data-qa="miles-' + index + '-edit"]'; }

  setLengthUnitsQuestion(index = 0) { return '#set-length-units-question-' + index; }

  durationHour(index = 0) { return '#duration-hour-' + index + '-answer'; }

  durationHourEdit(index = 0) { return '[data-qa="duration-hour-' + index + '-edit"]'; }

  durationYear(index = 0) { return '#duration-year-' + index + '-answer'; }

  durationYearEdit(index = 0) { return '[data-qa="duration-year-' + index + '-edit"]'; }

  setDurationUnitsQuestion(index = 0) { return '#set-duration-units-question-' + index; }

  squareCentimetres(index = 0) { return '#square-centimetres-' + index + '-answer'; }

  squareCentimetresEdit(index = 0) { return '[data-qa="square-centimetres-' + index + '-edit"]'; }

  squareMetres(index = 0) { return '#square-metres-' + index + '-answer'; }

  squareMetresEdit(index = 0) { return '[data-qa="square-metres-' + index + '-edit"]'; }

  squareKilometres(index = 0) { return '#square-kilometres-' + index + '-answer'; }

  squareKilometresEdit(index = 0) { return '[data-qa="square-kilometres-' + index + '-edit"]'; }

  squareMiles(index = 0) { return '#square-miles-' + index + '-answer'; }

  squareMilesEdit(index = 0) { return '[data-qa="square-miles-' + index + '-edit"]'; }

  acres(index = 0) { return '#acres-' + index + '-answer'; }

  acresEdit(index = 0) { return '[data-qa="acres-' + index + '-edit"]'; }

  hectares(index = 0) { return '#hectares-' + index + '-answer'; }

  hectaresEdit(index = 0) { return '[data-qa="hectares-' + index + '-edit"]'; }

  setAreaUnitQuestions(index = 0) { return '#set-area-unit-questions-' + index; }

  cubicCentimetres(index = 0) { return '#cubic-centimetres-' + index + '-answer'; }

  cubicCentimetresEdit(index = 0) { return '[data-qa="cubic-centimetres-' + index + '-edit"]'; }

  cubicMetres(index = 0) { return '#cubic-metres-' + index + '-answer'; }

  cubicMetresEdit(index = 0) { return '[data-qa="cubic-metres-' + index + '-edit"]'; }

  litres(index = 0) { return '#litres-' + index + '-answer'; }

  litresEdit(index = 0) { return '[data-qa="litres-' + index + '-edit"]'; }

  hectolitres(index = 0) { return '#hectolitres-' + index + '-answer'; }

  hectolitresEdit(index = 0) { return '[data-qa="hectolitres-' + index + '-edit"]'; }

  megalitres(index = 0) { return '#megalitres-' + index + '-answer'; }

  megalitresEdit(index = 0) { return '[data-qa="megalitres-' + index + '-edit"]'; }

  setVolumeUnitQuestions(index = 0) { return '#set-volume-unit-questions-' + index; }

  testTitle(index = 0) { return '#test-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
