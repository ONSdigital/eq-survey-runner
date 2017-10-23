// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class DateBlockPage extends QuestionPage {

  constructor() {
    super('date-block');
  }

  dateRangeFromday() {
    return '#date-range-from-day';
  }

  dateRangeFrommonth() {
    return '#date-range-from-month';
  }

  dateRangeFromyear() {
    return '#date-range-from-year';
  }

  dateRangeToday() {
    return '#date-range-to-day';
  }

  dateRangeTomonth() {
    return '#date-range-to-month';
  }

  dateRangeToyear() {
    return '#date-range-to-year';
  }

  monthYearMonth() {
    return '#month-year-answer-month';
  }

  monthYearanswerYear() {
    return '#month-year-answer-year';
  }

  singleDateday() {
    return '#single-date-answer-day';
  }

  singleDatemonth() {
    return '#single-date-answer-month';
  }

  singleDateyear() {
    return '#single-date-answer-year';
  }

  nonMandatoryDateday() {
    return '#non-mandatory-date-answer-day';
  }

  nonMandatoryDatemonth() {
    return '#non-mandatory-date-answer-month';
  }

  nonMandatoryDateyear() {
    return '#non-mandatory-date-answer-year';
  }

  dayLabel() {
    return '#label-single-date-answer-day';
  }
}
module.exports = new DateBlockPage();
