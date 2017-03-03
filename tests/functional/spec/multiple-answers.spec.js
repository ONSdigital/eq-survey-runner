import {getRandomString, openQuestionnaire} from '../helpers'
import personalDetailsPage from '../pages/surveys/answers/personal-details.page'
import multipleAnswerSummaryPage from '../pages/surveys/answers/multiple-answer-summary.page'


describe('Error messages', function() {

  it('Given a survey has multiple answers for a question when I save the survey then the summary shows all the answers', function() {
    // Given
    openQuestionnaire('multiple_answers.json')

    // When
    personalDetailsPage.setFirstName('Han')
      .setSurname('Solo')
      .submit()

    // Then
    expect(multipleAnswerSummaryPage.getFirstName()).to.equal('Han')
    expect(multipleAnswerSummaryPage.getSurname()).to.equal('Solo')
  })

  it('Given I complete a survey that has multiple answers for a question when I edit an answer then I appear on the page to edit my answer', function() {
    // Given
    openQuestionnaire('multiple_answers.json')
    personalDetailsPage.setFirstName('Han')
      .setSurname('Solo')
      .submit()

    // When
    multipleAnswerSummaryPage.editSurname()

    // Then
    expect(personalDetailsPage.isOpen()).to.be.true
  })

})
