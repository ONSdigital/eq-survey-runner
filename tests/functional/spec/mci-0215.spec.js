import {startQuestionnaire} from '../helpers'
import {openQuestionnaire} from '../helpers'

import landingPage from '../pages/landing.page'
import Introduction from '../pages/surveys/mci-0215/introduction.page.js'
import ReportingPeriod from '../pages/surveys/mci-0215/reporting-period.page.js'
import TotalRetailTurnoverBlock from '../pages/surveys/mci-0215/total-retail-turnover-block.page.js'
import FoodSales from '../pages/surveys/mci-0215/food-sales.page.js'
import AlcoholSales from '../pages/surveys/mci-0215/alcohol-sales.page.js'
import ClothingSales from '../pages/surveys/mci-0215/clothing-sales.page.js'
import HouseholdGoodsSales from '../pages/surveys/mci-0215/household-goods-sales.page.js'
import OtherGoodsSales from '../pages/surveys/mci-0215/other-goods-sales.page.js'
import TotalInternetSales from '../pages/surveys/mci-0215/total-internet-sales.page.js'
import AutomotiveFuel from '../pages/surveys/mci-0215/automotive-fuel.page.js'
import SignificantChange from '../pages/surveys/mci-0215/significant-change.page.js'
import ReasonForChange from '../pages/surveys/mci-0215/reason-for-change.page.js'
import ChangeCommentBlock from '../pages/surveys/mci-0215/change-comment-block.page.js'
import TotalEmployees from '../pages/surveys/mci-0215/total-employees.page.js'
import EmployeesBreakdown from '../pages/surveys/mci-0215/employees-breakdown.page.js'
import Summary from '../pages/surveys/mci-0215/summary.page.js'
import thankYou from '../pages/thank-you.page'


describe('MCI 0215 Test', function() {

  it('Given the mci business survey 0215 is selected when I start the survey then the landing page is displayed', function() {
    // Given
    // When
    openQuestionnaire('1_0215.json')

    // Then
    expect(landingPage.isOpen(), 'Landing page should be open').to.be.true
  })

  it('Given the mci business survey 0215 has been started when I complete the survey then I reach the thank you page', function() {
    // Given
    startQuestionnaire('1_0215.json')

    // When
    ReportingPeriod.setPeriodFromDay('01')
        .setPeriodFromMonth(5)
        .setPeriodFromYear('2016')
        .setPeriodToDay('31')
        .setPeriodToMonth(5)
        .setPeriodToYear('2016')
        .submit()

    TotalRetailTurnoverBlock.setTotalRetailTurnover('1234567')
        .submit()

    FoodSales.setTotalSalesFood('7')
        .submit()

    AlcoholSales.setTotalSalesAlcohol('60')
        .submit()

    ClothingSales.setTotalSalesClothing('500')
        .submit()

    HouseholdGoodsSales.setTotalSalesHouseholdGoods('4000')
        .submit()

    OtherGoodsSales.setTotalSalesOtherGoods('30000')
        .submit()

    TotalInternetSales.setInternetSales('200000')
        .submit()

    AutomotiveFuel.setTotalSalesAutomotiveFuel('1000000')
        .submit()

    SignificantChange.clickSignificantChangeEstablishedAnswerYes()
        .submit()

    ReasonForChange.clickReasonForChangeAnswerWeather()
        .submit()

    ChangeCommentBlock.setChangeComment('Bad weather reduced shop footfall')
        .submit()

    TotalEmployees.setTotalNumberEmployees('100')
        .submit()

    EmployeesBreakdown.setNumberMaleEmployeesOver30Hours('10')
        .setNumberMaleEmployeesUnder30Hours('20')
        .setNumberFemaleEmployeesOver30Hours('30')
        .setNumberFemaleEmployeesUnder30Hours('40')
        .submit()

    Summary.submit()

    // Then
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })

  it('Given the mci business survey 0215 has been started and sales questions completed when I select No for significant changes I skip to total employees question', function() {
    // Given
    startQuestionnaire('1_0215.json')

    ReportingPeriod.setPeriodFromDay('01')
        .setPeriodFromMonth(5)
        .setPeriodFromYear('2016')
        .setPeriodToDay('31')
        .setPeriodToMonth(5)
        .setPeriodToYear('2016')
        .submit()

    TotalRetailTurnoverBlock.setTotalRetailTurnover('0')
        .submit()
    FoodSales.submit()
    AlcoholSales.submit()
    ClothingSales.submit()
    HouseholdGoodsSales.submit()
    OtherGoodsSales.submit()
    TotalInternetSales.submit()
    AutomotiveFuel.submit()

    // When
    SignificantChange.clickSignificantChangeEstablishedAnswerNo()
        .submit()

    // Then
    expect(TotalEmployees.isOpen(), 'Total Employees page should be open').to.be.true
  })

})

