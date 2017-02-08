import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import DatesPage from '../pages/surveys/dates/dates-answers.page'
import SummaryPage from '../pages/surveys/dates/dates-summary.page'

const expect = chai.expect

describe('Date checks', function() {

      it('Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted', function() {

            // Given the test_dates survey is selected
            startQuestionnaire('test_dates.json')

            // When dates are entered
            DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(3)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodDay(3)
              .setToReportingPeriodMonth(5)
              .setToReportingPeriodYear(2017)
              .setMonthYearMonth(4)
              .setMonthYearYear(2018)
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)
              .submit()

            // Then the summary screen shows the dates entered formatted
            expect(SummaryPage.getDateRangeSummary()).to.contain('01 March 2016 to 03 May 2017')
            expect(SummaryPage.getMonthYearDateSummary()).to.contain('April 2018')
            expect(SummaryPage.getDateOfBirth()).to.contain('04 January 1999')
            expect(SummaryPage.getNonMandatoryDate()).to.contain('No answer provided')

        })


      it('Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown', function() {

            // Given the test_dates survey is selected
             startQuestionnaire('test_dates.json')

            // When the from date is greater than the to date
            DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(1)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodDay(1)
              .setToReportingPeriodMonth(1)
              .setToReportingPeriodYear(2015)
              .setMonthYearYear(2018)
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)
              .submit()

            // Then an error message is shown
            expect(DatesPage.getAlertText()).to.contain('The \'period to\' date cannot be before the \'period from\' date.')

        })

      it('Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown', function() {

            // Given the test_dates survey is selected
             startQuestionnaire('test_dates.json')

            // When the from date and the to date are the same
            DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(1)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodDay(1)
              .setToReportingPeriodMonth(1)
              .setToReportingPeriodYear(2016)
              .setMonthYearYear(2018)
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)
              .submit()

            // Then an error message is shown
            expect(DatesPage.getAlertText()).to.contain('The \'period to\' date must be different to the \'period from\' date.')

        })

      it('Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown', function() {

            // Given the test_dates survey is selected
             startQuestionnaire('test_dates.json')

            // When an invalid date is entered in a date range
            DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(1)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodDay(3)
              .setToReportingPeriodMonth(1)
              .setToReportingPeriodYear('')
              .setMonthYearYear(2018)
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)
              .submit()

            // Then an error message is shown
            expect(DatesPage.getAlertText()).to.contain('The date entered is not valid. Please correct your answer.')

        })

      it('Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown', function() {

            // Given the test_dates survey is selected
             startQuestionnaire('test_dates.json')

            // When the year (month year type) is left empty
            DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(1)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodMonth(1)
              .setToReportingPeriodDay(3)
              .setToReportingPeriodYear(2017)
              .setMonthYearMonth(1)
              .setMonthYearYear('')
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)
              .submit()

            // Then an error message is shown
            expect(DatesPage.getAlertText()).to.contain('The date entered is not valid. Please correct your answer.')

        })

      it('Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct', function() {

            // Given the test_dates survey is selected
            startQuestionnaire('test_dates.json')

            // When an error message is shown
            DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(1)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodDay(3)
              .setToReportingPeriodMonth(1)
              .setToReportingPeriodYear(2017)
              .setMonthYearMonth(1)
              .setMonthYearYear('')
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)
              .submit()

            expect(DatesPage.getAlertText()).to.contain('The date entered is not valid. Please correct your answer.')


            // Then when it is corrected, it goes to the summary page and the information is correct
             DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(1)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodDay(3)
              .setToReportingPeriodMonth(1)
              .setToReportingPeriodYear(2017)
              .setMonthYearMonth(6)
              .setMonthYearYear('2018')
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)
              .submit()

            expect(SummaryPage.getDateRangeSummary()).to.contain('01 January 2016 to 03 January 2017')
            expect(SummaryPage.getMonthYearDateSummary()).to.contain('June 2018')

      })

      it('Given the test_dates survey is selected when a partially completed optional date is submitted, an error is shown', function() {
            // Given the test_dates survey is selected
            startQuestionnaire('test_dates.json')

            // Setup the mandatory stuff
            DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(1)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodDay(3)
              .setToReportingPeriodMonth(1)
              .setToReportingPeriodYear(2017)
              .setMonthYearMonth(6)
              .setMonthYearYear(2018)
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)

            // When
            DatesPage.setNonMandatoryDateAnswerDay(1)
                     .setNonMandatoryDateAnswerMonth(10)
                     .submit()
            // Then
            expect(DatesPage.getAlertText()).to.contain('The date entered is not valid. Please correct your answer.')
      })

      it('Given a optional date is successfully submitted, when the date is edited, it should then be possible to select an empty month', function() {
            // Given the test_dates survey is selected
            startQuestionnaire('test_dates.json')

            // Setup the mandatory stuff
            DatesPage.setFromReportingPeriodDay(1)
              .setFromReportingPeriodMonth(1)
              .setFromReportingPeriodYear(2016)
              .setToReportingPeriodDay(3)
              .setToReportingPeriodMonth(1)
              .setToReportingPeriodYear(2017)
              .setMonthYearMonth(6)
              .setMonthYearYear(2018)
              .setDateOfBirthDay(4)
              .setDateOfBirthMonth(1)
              .setDateOfBirthYear(1999)

            DatesPage.setNonMandatoryDateAnswerDay(12)
              .setNonMandatoryDateAnswerMonth(1)
              .setNonMandatoryDateAnswerYear(2016)
              .submit()

            expect(SummaryPage.getDateRangeSummary()).to.contain('01 January 2016 to 03 January 2017')
            expect(SummaryPage.getMonthYearDateSummary()).to.contain('June 2018')

            // When
            SummaryPage.editNonMandatoryDate()

            DatesPage.setNonMandatoryDateAnswerMonth('')
              .submit()

            // Then
            expect(DatesPage.getAlertText()).to.contain('The date entered is not valid. Please correct your answer.')
      })

      it('Given the test_dates survey is selected, when a user clicks the day label then the day subfield should gain the focus', function() {

            // Given the test_dates survey is selected
            startQuestionnaire('test_dates.json')

            // When a user clicks the day label
            DatesPage.dayLabel.click()

            // Then the day subfield should gain the focus
            expect(browser.hasFocus(DatesPage.dayInput.selector)).to.be.true
      })
})
