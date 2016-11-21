import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import FinalConfirmationSurveyPage from '../pages/surveys/confirmation/final-confirmation-survey.page'
import Confirmation from '../pages/confirmation.page'
import ThankYou from '../pages/thank-you.page'

const expect = chai.expect

describe('Final confirmation before submit', function () {

    var confirmation_schema = 'test_final_confirmation.json';

    it('Given I successfully complete a questionnaire, when I submit the page, then I should be prompted for confirmation to submit.', function () {
        //Given
        startQuestionnaire(confirmation_schema)

        // When
        FinalConfirmationSurveyPage.setBreakfastFood('Bacon').submit()

        //Then
        expect(Confirmation.getSubtitle()).to.contain('Thank you for your answers, do you wish to submit')
    })

    it('Given I successfully complete a questionnaire, when I confirm submit, then the submission is successful', function () {
        //Given
        startQuestionnaire(confirmation_schema)
        FinalConfirmationSurveyPage.setBreakfastFood('Bacon').submit()

        // When
        Confirmation.submit()

        //Then
        expect(ThankYou.getMainHeading()).to.contain('Submission Successful')
    })


    it('Given I successfully complete a questionnaire and am on the confirmation page, when I click change answers, then I should be returned to the questionnaire', function () {
        //Given
        startQuestionnaire(confirmation_schema)
        FinalConfirmationSurveyPage.setBreakfastFood('Bacon').submit()

        // When
        Confirmation.changeAnswers()

        //Then
        expect(FinalConfirmationSurveyPage.isOpen()).to.be.true
    })

})
