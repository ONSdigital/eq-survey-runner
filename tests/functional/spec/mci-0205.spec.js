import {getRandomString, openQuestionnaire, startQuestionnaire} from '../helpers'
import landingPage from '../pages/landing.page'
import Introduction from '../pages/surveys/mci/introduction.page.js'
import ReportingPeriod from '../pages/surveys/mci/reporting-period.page.js'
import TotalRetailTurnoverBlock from '../pages/surveys/mci/total-retail-turnover-block.page.js'
import FoodSales from '../pages/surveys/mci/food-sales.page.js'
import AlcoholSales from '../pages/surveys/mci/alcohol-sales.page.js'
import ClothingSales from '../pages/surveys/mci/clothing-sales.page.js'
import HouseholdGoodsSales from '../pages/surveys/mci/household-goods-sales.page.js'
import OtherGoodsSales from '../pages/surveys/mci/other-goods-sales.page.js'
import TotalInternetSales from '../pages/surveys/mci/total-internet-sales.page.js'
import AutomotiveFuel from '../pages/surveys/mci/automotive-fuel.page.js'
import SignificantChange from '../pages/surveys/mci/significant-change.page.js'
import ReasonForChange from '../pages/surveys/mci/reason-for-change.page.js'
import ChangeCommentBlock from '../pages/surveys/mci/change-comment-block.page.js'
import Summary from '../pages/surveys/mci/summary.page.js'
import thankYou from '../pages/thank-you.page'

describe('MCI 0205 Test', function() {

  it('Given the mci business survey 0205 is selected when I start the survey then the landing page is displayed', function() {
    // Given
    // When
    openQuestionnaire('1_0205.json', getRandomString(10), getRandomString(5))

    // Then
    expect(landingPage.isOpen(), 'Landing page should be open').to.be.true
  })

  it('Given the mci business survey 0205 has been started when I complete the survey then I reach the thank you page', function() {
    // Given
    startQuestionnaire('1_0205.json', getRandomString(10), getRandomString(5))

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

    Summary.submit()

    // Then
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })

  it('Given the mci business survey 0205 has been started and sales questions completed when I select No for significant changes I skip to total employees question', function() {
    // Given
    startQuestionnaire('1_0205.json', getRandomString(10), getRandomString(5))

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

    Summary.submit()

    // Then
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })

})
