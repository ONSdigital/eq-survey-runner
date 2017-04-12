import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import PayPatternFrequency from '../pages/surveys/mwss/pay-pattern-frequency.page.js'
import WeeklyPayIntroduction from '../pages/surveys/mwss/weekly-pay-introduction.page.js'
import WeeklyPayPaidEmployees from '../pages/surveys/mwss/weekly-pay-paid-employees.page.js'
import WeeklyPayGrossPay from '../pages/surveys/mwss/weekly-pay-gross-pay.page.js'
import WeeklyPayBreakdown from '../pages/surveys/mwss/weekly-pay-breakdown.page.js'
import WeeklyPaySignificantChangesPaidEmployees from '../pages/surveys/mwss/weekly-pay-significant-changes-paid-employees.page.js'
import WeeklyPaySignificantChangesRedundancies from '../pages/surveys/mwss/weekly-pay-significant-changes-redundancies.page.js'
import WeeklyPaySignificantChangesTempEmployees from '../pages/surveys/mwss/weekly-pay-significant-changes-temp-employees.page.js'
import WeeklyPaySignificantChangesGrossPay from '../pages/surveys/mwss/weekly-pay-significant-changes-gross-pay.page.js'
import WeeklyPaySignificantChangesOvertime from '../pages/surveys/mwss/weekly-pay-significant-changes-overtime.page.js'
import WeeklyPaySignificantChangesPayRates from '../pages/surveys/mwss/weekly-pay-significant-changes-pay-rates.page.js'
import WeeklyPaySignificantChangesPayRatesIncrease from '../pages/surveys/mwss/weekly-pay-significant-changes-pay-rates-increase.page.js'
import WeeklyPaySignificantChangesIndustrialAction from '../pages/surveys/mwss/weekly-pay-significant-changes-industrial-action.page.js'
import WeeklyPaySignificantChangesOther from '../pages/surveys/mwss/weekly-pay-significant-changes-other.page.js'
import WeeklyPaySignificantChangesOtherSpecify from '../pages/surveys/mwss/weekly-pay-significant-changes-other-specify.page.js'
import FortnightlyPayIntroduction from '../pages/surveys/mwss/fortnightly-pay-introduction.page.js'
import FortnightlyPayPaidEmployees from '../pages/surveys/mwss/fortnightly-pay-paid-employees.page.js'
import FortnightlyPayGrossPay from '../pages/surveys/mwss/fortnightly-pay-gross-pay.page.js'
import FortnightlyPayBreakdown from '../pages/surveys/mwss/fortnightly-pay-breakdown.page.js'
import FortnightlyPaySignificantChangesPaidEmployees from '../pages/surveys/mwss/fortnightly-pay-significant-changes-paid-employees.page.js'
import FortnightlyPaySignificantChangesRedundancies from '../pages/surveys/mwss/fortnightly-pay-significant-changes-redundancies.page.js'
import FortnightlyPaySignificantChangesTempEmployees from '../pages/surveys/mwss/fortnightly-pay-significant-changes-temp-employees.page.js'
import FortnightlyPaySignificantChangesGrossPay from '../pages/surveys/mwss/fortnightly-pay-significant-changes-gross-pay.page.js'
import FortnightlyPaySignificantChangesOvertime from '../pages/surveys/mwss/fortnightly-pay-significant-changes-overtime.page.js'
import FortnightlyPaySignificantChangesPayRates from '../pages/surveys/mwss/fortnightly-pay-significant-changes-pay-rates.page.js'
import FortnightlyPaySignificantChangesPayRatesIncrease from '../pages/surveys/mwss/fortnightly-pay-significant-changes-pay-rates-increase.page.js'
import FortnightlyPaySignificantChangesIndustrialAction from '../pages/surveys/mwss/fortnightly-pay-significant-changes-industrial-action.page.js'
import FortnightlyPaySignificantChangesOther from '../pages/surveys/mwss/fortnightly-pay-significant-changes-other.page.js'
import FortnightlyPaySignificantChangesOtherSpecify from '../pages/surveys/mwss/fortnightly-pay-significant-changes-other-specify.page.js'
import CalendarMonthlyPayIntroduction from '../pages/surveys/mwss/calendar-monthly-pay-introduction.page.js'
import CalendarMonthlyPayPaidEmployees from '../pages/surveys/mwss/calendar-monthly-pay-paid-employees.page.js'
import CalendarMonthlyPayGrossPay from '../pages/surveys/mwss/calendar-monthly-pay-gross-pay.page.js'
import CalendarMonthlyPayBreakdown from '../pages/surveys/mwss/calendar-monthly-pay-breakdown.page.js'
import CalendarMonthlyPaySignificantChangesPaidEmployees from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-paid-employees.page.js'
import CalendarMonthlyPaySignificantChangesRedundancies from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-redundancies.page.js'
import CalendarMonthlyPaySignificantChangesTempEmployees from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-temp-employees.page.js'
import CalendarMonthlyPaySignificantChangesGrossPay from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-gross-pay.page.js'
import CalendarMonthlyPaySignificantChangesOvertime from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-overtime.page.js'
import CalendarMonthlyPaySignificantChangesPayRates from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-pay-rates.page.js'
import CalendarMonthlyPaySignificantChangesPayRatesIncrease from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-pay-rates-increase.page.js'
import CalendarMonthlyPaySignificantChangesIndustrialAction from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-industrial-action.page.js'
import CalendarMonthlyPaySignificantChangesOther from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-other.page.js'
import CalendarMonthlyPaySignificantChangesOtherSpecify from '../pages/surveys/mwss/calendar-monthly-pay-significant-changes-other-specify.page.js'
import FourWeeklyPayIntroduction from '../pages/surveys/mwss/four-weekly-pay-introduction.page.js'
import FourWeeklyPayPaidEmployees from '../pages/surveys/mwss/four-weekly-pay-paid-employees.page.js'
import FourWeeklyPayGrossPay from '../pages/surveys/mwss/four-weekly-pay-gross-pay.page.js'
import FourWeeklyPayBreakdown from '../pages/surveys/mwss/four-weekly-pay-breakdown.page.js'
import FourWeeklyPaySignificantChangesPaidEmployees from '../pages/surveys/mwss/four-weekly-pay-significant-changes-paid-employees.page.js'
import FourWeeklyPaySignificantChangesRedundancies from '../pages/surveys/mwss/four-weekly-pay-significant-changes-redundancies.page.js'
import FourWeeklyPaySignificantChangesTempEmployees from '../pages/surveys/mwss/four-weekly-pay-significant-changes-temp-employees.page.js'
import FourWeeklyPaySignificantChangesGrossPay from '../pages/surveys/mwss/four-weekly-pay-significant-changes-gross-pay.page.js'
import FourWeeklyPaySignificantChangesOvertime from '../pages/surveys/mwss/four-weekly-pay-significant-changes-overtime.page.js'
import FourWeeklyPaySignificantChangesPayRates from '../pages/surveys/mwss/four-weekly-pay-significant-changes-pay-rates.page.js'
import FourWeeklyPaySignificantChangesPayRatesIncrease from '../pages/surveys/mwss/four-weekly-pay-significant-changes-pay-rates-increase.page.js'
import FourWeeklyPaySignificantChangesIndustrialAction from '../pages/surveys/mwss/four-weekly-pay-significant-changes-industrial-action.page.js'
import FourWeeklyPaySignificantChangesOther from '../pages/surveys/mwss/four-weekly-pay-significant-changes-other.page.js'
import FourWeeklyPaySignificantChangesOtherSpecify from '../pages/surveys/mwss/four-weekly-pay-significant-changes-other-specify.page.js'
import FiveWeeklyPayIntroduction from '../pages/surveys/mwss/five-weekly-pay-introduction.page.js'
import FiveWeeklyPayPaidEmployees from '../pages/surveys/mwss/five-weekly-pay-paid-employees.page.js'
import FiveWeeklyPayGrossPay from '../pages/surveys/mwss/five-weekly-pay-gross-pay.page.js'
import FiveWeeklyPayBreakdown from '../pages/surveys/mwss/five-weekly-pay-breakdown.page.js'
import FiveWeeklyPaySignificantChangesPaidEmployees from '../pages/surveys/mwss/five-weekly-pay-significant-changes-paid-employees.page.js'
import FiveWeeklyPaySignificantChangesRedundancies from '../pages/surveys/mwss/five-weekly-pay-significant-changes-redundancies.page.js'
import FiveWeeklyPaySignificantChangesTempEmployees from '../pages/surveys/mwss/five-weekly-pay-significant-changes-temp-employees.page.js'
import FiveWeeklyPaySignificantChangesGrossPay from '../pages/surveys/mwss/five-weekly-pay-significant-changes-gross-pay.page.js'
import FiveWeeklyPaySignificantChangesOvertime from '../pages/surveys/mwss/five-weekly-pay-significant-changes-overtime.page.js'
import FiveWeeklyPaySignificantChangesPayRates from '../pages/surveys/mwss/five-weekly-pay-significant-changes-pay-rates.page.js'
import FiveWeeklyPaySignificantChangesPayRatesIncrease from '../pages/surveys/mwss/five-weekly-pay-significant-changes-pay-rates-increase.page.js'
import FiveWeeklyPaySignificantChangesIndustrialAction from '../pages/surveys/mwss/five-weekly-pay-significant-changes-industrial-action.page.js'
import FiveWeeklyPaySignificantChangesOther from '../pages/surveys/mwss/five-weekly-pay-significant-changes-other.page.js'
import FiveWeeklyPaySignificantChangesOtherSpecify from '../pages/surveys/mwss/five-weekly-pay-significant-changes-other-specify.page.js'
import GeneralCommentsIntroduction from '../pages/surveys/mwss/general-comments-introduction.page.js'
import GeneralComments from '../pages/surveys/mwss/general-comments.page.js'
import SummaryPage from '../pages/summary.page'
import ThankYou from '../pages/thank-you.page'


const expect = chai.expect

describe('MWSS Core', function() {

    it('Given I am completing MWSS, When I have all pay patters, Then I can submit data for every pattern', function() {
        startQuestionnaire('1_0005.json')

        PayPatternFrequency.clickPayPatternFrequencyAnswerWeekly()
        PayPatternFrequency.clickPayPatternFrequencyAnswerFortnightly()
        PayPatternFrequency.clickPayPatternFrequencyAnswerCalendarMonthly()
        PayPatternFrequency.clickPayPatternFrequencyAnswerFourWeekly()
        PayPatternFrequency.clickPayPatternFrequencyAnswerFiveWeekly()
        PayPatternFrequency.submit()

        // Weekly Pay
        WeeklyPayIntroduction.submit()
        WeeklyPayPaidEmployees.setWeeklyPayPaidEmployeesAnswer(5).submit()
        WeeklyPayGrossPay.setWeeklyPayGrossPayAnswer(445566).submit()

        WeeklyPayBreakdown.setWeeklyPayBreakdownHolidayAnswer(112233)
        WeeklyPayBreakdown.setWeeklyPayBreakdownArrearsAnswer(334455)
        WeeklyPayBreakdown.setWeeklyPayBreakdownPrpAnswer(556677)
        WeeklyPayBreakdown.submit()

        WeeklyPaySignificantChangesPaidEmployees.clickWeeklyPaySignificantChangesPaidEmployeesAnswerYes().submit()
        WeeklyPaySignificantChangesRedundancies.clickWeeklyPaySignificantChangesRedundanciesAnswerYes().submit()
        WeeklyPaySignificantChangesTempEmployees.clickWeeklyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff().submit()
        WeeklyPaySignificantChangesGrossPay.clickWeeklyPaySignificantChangesGrossPayAnswerYes().submit()
        WeeklyPaySignificantChangesOvertime.clickWeeklyPaySignificantChangesOvertimeAnswerMoreOvertime().submit()
        WeeklyPaySignificantChangesPayRates.clickWeeklyPaySignificantChangesPayRatesAnswerYes().submit()

        WeeklyPaySignificantChangesPayRatesIncrease.setWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(50)
        WeeklyPaySignificantChangesPayRatesIncrease.setWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(1)
        WeeklyPaySignificantChangesPayRatesIncrease.setWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(2)
        WeeklyPaySignificantChangesPayRatesIncrease.setWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(2016)
        WeeklyPaySignificantChangesPayRatesIncrease.setWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(25)
        WeeklyPaySignificantChangesPayRatesIncrease.submit()

        WeeklyPaySignificantChangesIndustrialAction.clickWeeklyPaySignificantChangesIndustrialActionAnswerYes().submit()
        WeeklyPaySignificantChangesOther.clickWeeklyPaySignificantChangesOtherAnswerYes().submit()
        WeeklyPaySignificantChangesOtherSpecify.setWeeklyPaySignificantChangesOtherSpecifyAnswer('Pipe mania').submit()


        // Fortnightly Pay
        FortnightlyPayIntroduction.submit()
        FortnightlyPayPaidEmployees.setFortnightlyPayPaidEmployeesAnswer(10).submit()
        FortnightlyPayGrossPay.setFortnightlyPayGrossPayAnswer(123123).submit()

        FortnightlyPayBreakdown.setFortnightlyPayBreakdownHolidayAnswer(456456)
        FortnightlyPayBreakdown.setFortnightlyPayBreakdownArrearsAnswer(789789)
        FortnightlyPayBreakdown.setFortnightlyPayBreakdownPrpAnswer(101010)
        FortnightlyPayBreakdown.submit()

        FortnightlyPaySignificantChangesPaidEmployees.clickFortnightlyPaySignificantChangesPaidEmployeesAnswerYes().submit()
        FortnightlyPaySignificantChangesRedundancies.clickFortnightlyPaySignificantChangesRedundanciesAnswerYes().submit()
        FortnightlyPaySignificantChangesTempEmployees.clickFortnightlyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff().submit()
        FortnightlyPaySignificantChangesGrossPay.clickFortnightlyPaySignificantChangesGrossPayAnswerYes().submit()
        FortnightlyPaySignificantChangesOvertime.clickFortnightlyPaySignificantChangesOvertimeAnswerMoreOvertime().submit()
        FortnightlyPaySignificantChangesPayRates.clickFortnightlyPaySignificantChangesPayRatesAnswerYes().submit()

        FortnightlyPaySignificantChangesPayRatesIncrease.setFortnightlyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(60)
        FortnightlyPaySignificantChangesPayRatesIncrease.setFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(2)
        FortnightlyPaySignificantChangesPayRatesIncrease.setFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(3)
        FortnightlyPaySignificantChangesPayRatesIncrease.setFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(2017)
        FortnightlyPaySignificantChangesPayRatesIncrease.setFortnightlyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(30)
        FortnightlyPaySignificantChangesPayRatesIncrease.submit()

        FortnightlyPaySignificantChangesIndustrialAction.clickFortnightlyPaySignificantChangesIndustrialActionAnswerYes().submit()
        FortnightlyPaySignificantChangesOther.clickFortnightlyPaySignificantChangesOtherAnswerYes().submit()
        FortnightlyPaySignificantChangesOtherSpecify.setFortnightlyPaySignificantChangesOtherSpecifyAnswer('Gas leak').submit()


        // Calendar Monthly Pay
        CalendarMonthlyPayIntroduction.submit()
        CalendarMonthlyPayPaidEmployees.setCalendarMonthlyPayPaidEmployeesAnswer(20).submit()
        CalendarMonthlyPayGrossPay.setCalendarMonthlyPayGrossPayAnswer(321321).submit()

        CalendarMonthlyPayBreakdown.setCalendarMonthlyPayBreakdownArrearsAnswer(121212)
        CalendarMonthlyPayBreakdown.setCalendarMonthlyPayBreakdownPrpAnswer(999999)
        CalendarMonthlyPayBreakdown.submit()

        CalendarMonthlyPaySignificantChangesPaidEmployees.clickCalendarMonthlyPaySignificantChangesPaidEmployeesAnswerYes().submit()
        CalendarMonthlyPaySignificantChangesRedundancies.clickCalendarMonthlyPaySignificantChangesRedundanciesAnswerYes().submit()
        CalendarMonthlyPaySignificantChangesTempEmployees.clickCalendarMonthlyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff().submit()
        CalendarMonthlyPaySignificantChangesGrossPay.clickCalendarMonthlyPaySignificantChangesGrossPayAnswerYes().submit()
        CalendarMonthlyPaySignificantChangesOvertime.clickCalendarMonthlyPaySignificantChangesOvertimeAnswerMoreOvertime().submit()
        CalendarMonthlyPaySignificantChangesPayRates.clickCalendarMonthlyPaySignificantChangesPayRatesAnswerYes().submit()

        CalendarMonthlyPaySignificantChangesPayRatesIncrease.setCalendarMonthlyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(70)
        CalendarMonthlyPaySignificantChangesPayRatesIncrease.setCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(3)
        CalendarMonthlyPaySignificantChangesPayRatesIncrease.setCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(4)
        CalendarMonthlyPaySignificantChangesPayRatesIncrease.setCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(2018)
        CalendarMonthlyPaySignificantChangesPayRatesIncrease.setCalendarMonthlyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(40)
        CalendarMonthlyPaySignificantChangesPayRatesIncrease.submit()

        CalendarMonthlyPaySignificantChangesIndustrialAction.clickCalendarMonthlyPaySignificantChangesIndustrialActionAnswerYes().submit()
        CalendarMonthlyPaySignificantChangesOther.clickCalendarMonthlyPaySignificantChangesOtherAnswerYes().submit()
        CalendarMonthlyPaySignificantChangesOtherSpecify.setCalendarMonthlyPaySignificantChangesOtherSpecifyAnswer('copper pipe').submit()


        // Four Weekly Pay
        FourWeeklyPayIntroduction.submit()
        FourWeeklyPayPaidEmployees.setFourWeeklyPayPaidEmployeesAnswer(30).submit()
        FourWeeklyPayGrossPay.setFourWeeklyPayGrossPayAnswer(98765).submit()

        FourWeeklyPayBreakdown.setFourWeeklyPayBreakdownArrearsAnswer(443322)
        FourWeeklyPayBreakdown.setFourWeeklyPayBreakdownPrpAnswer(767676)
        FourWeeklyPayBreakdown.submit()

        FourWeeklyPaySignificantChangesPaidEmployees.clickFourWeeklyPaySignificantChangesPaidEmployeesAnswerYes().submit()
        FourWeeklyPaySignificantChangesRedundancies.clickFourWeeklyPaySignificantChangesRedundanciesAnswerYes().submit()
        FourWeeklyPaySignificantChangesTempEmployees.clickFourWeeklyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff().submit()
        FourWeeklyPaySignificantChangesGrossPay.clickFourWeeklyPaySignificantChangesGrossPayAnswerYes().submit()
        FourWeeklyPaySignificantChangesOvertime.clickFourWeeklyPaySignificantChangesOvertimeAnswerMoreOvertime().submit()
        FourWeeklyPaySignificantChangesPayRates.clickFourWeeklyPaySignificantChangesPayRatesAnswerYes().submit()

        FourWeeklyPaySignificantChangesPayRatesIncrease.setFourWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(80)
        FourWeeklyPaySignificantChangesPayRatesIncrease.setFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(4)
        FourWeeklyPaySignificantChangesPayRatesIncrease.setFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(5)
        FourWeeklyPaySignificantChangesPayRatesIncrease.setFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(2019)
        FourWeeklyPaySignificantChangesPayRatesIncrease.setFourWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(50)
        FourWeeklyPaySignificantChangesPayRatesIncrease.submit()

        FourWeeklyPaySignificantChangesIndustrialAction.clickFourWeeklyPaySignificantChangesIndustrialActionAnswerYes().submit()
        FourWeeklyPaySignificantChangesOther.clickFourWeeklyPaySignificantChangesOtherAnswerYes().submit()
        FourWeeklyPaySignificantChangesOtherSpecify.setFourWeeklyPaySignificantChangesOtherSpecifyAnswer('solder joint').submit()


        // Five Weekly Pay
        FiveWeeklyPayIntroduction.submit()
        FiveWeeklyPayPaidEmployees.setFiveWeeklyPayPaidEmployeesAnswer(40).submit()
        FiveWeeklyPayGrossPay.setFiveWeeklyPayGrossPayAnswer(13134).submit()

        FiveWeeklyPayBreakdown.setFiveWeeklyPayBreakdownArrearsAnswer(989)
        FiveWeeklyPayBreakdown.setFiveWeeklyPayBreakdownPrpAnswer(9112)
        FiveWeeklyPayBreakdown.submit()

        FiveWeeklyPaySignificantChangesPaidEmployees.clickFiveWeeklyPaySignificantChangesPaidEmployeesAnswerYes().submit()
        FiveWeeklyPaySignificantChangesRedundancies.clickFiveWeeklyPaySignificantChangesRedundanciesAnswerYes().submit()
        FiveWeeklyPaySignificantChangesTempEmployees.clickFiveWeeklyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff().submit()
        FiveWeeklyPaySignificantChangesGrossPay.clickFiveWeeklyPaySignificantChangesGrossPayAnswerYes().submit()
        FiveWeeklyPaySignificantChangesOvertime.clickFiveWeeklyPaySignificantChangesOvertimeAnswerMoreOvertime().submit()
        FiveWeeklyPaySignificantChangesPayRates.clickFiveWeeklyPaySignificantChangesPayRatesAnswerYes().submit()

        FiveWeeklyPaySignificantChangesPayRatesIncrease.setFiveWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(90)
        FiveWeeklyPaySignificantChangesPayRatesIncrease.setFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(5)
        FiveWeeklyPaySignificantChangesPayRatesIncrease.setFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(6)
        FiveWeeklyPaySignificantChangesPayRatesIncrease.setFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(2020)
        FiveWeeklyPaySignificantChangesPayRatesIncrease.setFiveWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(60)
        FiveWeeklyPaySignificantChangesPayRatesIncrease.submit()

        FiveWeeklyPaySignificantChangesIndustrialAction.clickFiveWeeklyPaySignificantChangesIndustrialActionAnswerYes().submit()
        FiveWeeklyPaySignificantChangesOther.clickFiveWeeklyPaySignificantChangesOtherAnswerYes().submit()
        FiveWeeklyPaySignificantChangesOtherSpecify.setFiveWeeklyPaySignificantChangesOtherSpecifyAnswer('drill hole').submit()

        GeneralCommentsIntroduction.submit()
        GeneralComments.setGeneralCommentsAnswer('flux clean').submit()

        expect(SummaryPage.isOpen()).to.be.true
        SummaryPage.submit()

        expect(ThankYou.isOpen()).to.be.true
    })
})
