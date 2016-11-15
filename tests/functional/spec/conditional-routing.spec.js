
import chai from 'chai'
import {startQuestionnaire, getBlockId} from '../helpers'
import ConditionalRoutingPage from '../pages/surveys/conditional_routing/conditional-routing.page'

const expect = chai.expect

describe('Conditional routing.', function() {

  var basic_yes_no_question_schema = 'test_conditional_routing.json';

  it('Given a yes no question, when I select yes, I should be routed to the Yes response page.', function() {
    //Given
    startQuestionnaire(basic_yes_no_question_schema)

    //When
    ConditionalRoutingPage.clickYes().submit()

    // Then
    expect(getBlockId()).to.equal('response-yes')
  })

  it('Given a yes no question, when I select no, I should be routed to the No response page.', function() {
    //Given
    startQuestionnaire(basic_yes_no_question_schema)

    //When
    ConditionalRoutingPage.clickNo().submit()

    // Then
    expect(getBlockId()).to.equal('response-no')
  })

})
