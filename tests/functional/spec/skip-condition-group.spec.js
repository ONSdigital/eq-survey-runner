import {openQuestionnaire} from '../helpers'

import DoYouWantToSkipPage from '../pages/surveys/skip_condition_group/do-you-want-to-skip.page'
import LastGroupBlockPage from '../pages/surveys/skip_condition_group/last-group-block.page'


describe('Skip condition group', function() {

  it('Given I am being asked to skip a question, When I say Yes, Then I should skip the next group', function() {
    // Given
    openQuestionnaire('test_skip_condition_group.json')

    // When
    DoYouWantToSkipPage.clickDoYouWantToSkipAnswerYes().submit()

    // Then
    expect(LastGroupBlockPage.isOpen()).to.equal(true, 'Expected to skip next group')
  })

})
