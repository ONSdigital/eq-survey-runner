import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import InterstitialSurveyPage from '../pages/surveys/interstitial/interstitial-survey.page'
import InterstitialPage from '../pages/surveys/interstitial/breakfast-interstitial.page'
import SummaryPage from '../pages/surveys/interstitial/summary.page'

const expect = chai.expect

describe('Interstitial Pages', function () {

    var interstitial_schema = 'test_interstitial_page.json';

    it('Given I am completing a survey with an interstitial page, when I arrive at the interstitial page, then i should be able to continue the survey.', function () {
        //Given
        startQuestionnaire(interstitial_schema)
        InterstitialSurveyPage.setBreakfastFood('Cereal').submit()

        // When
        expect(InterstitialPage.getMainHeading()).to.contain('Breakfast Interstitial Page')

        //Then
        InterstitialPage.submit()
        InterstitialSurveyPage.setLunchFood('Soup').submit()
        expect(SummaryPage.getBreakfastAnswer()).to.contain('Cereal')
        expect(SummaryPage.getLunchAnswer()).to.contain('Soup')
    })

})
