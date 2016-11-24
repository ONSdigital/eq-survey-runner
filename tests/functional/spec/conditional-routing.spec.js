
import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import ConditionalRoutingPage from '../pages/surveys/conditional_routing/conditional-routing.page'

const expect = chai.expect

describe('Conditional routing for non repeating groups.', function() {

  var basic_yes_no_question_schema = 'test_conditional_routing.json';
  var repeating_and_conditional_routing_schema = 'test_repeating_and_conditional_routing.json';

  it('Given a yes no question, when I select yes, I should be routed to the Yes response page.', function() {
    //Given
    startQuestionnaire(basic_yes_no_question_schema)

    //When
    ConditionalRoutingPage.clickYes().submit()

    // Then
    expect(ConditionalRoutingPage.isBlock('response-yes')).to.be.true
  })

  it('Given a yes no question, when I select no, I should be routed to the No response page.', function() {
    //Given
    startQuestionnaire(basic_yes_no_question_schema)

    //When
    ConditionalRoutingPage.clickNo().submit()

    // Then
    expect(ConditionalRoutingPage.isBlock('response-no')).to.be.true
  })

})

describe('Conditional routing within repeating groups.', function() {

  var repeating_and_conditional_routing_schema = 'test_repeating_and_conditional_routing.json';

  it('Given n repeating groups, I should see the same questions repeated n times.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)

    //When
    var numberOfRepeats = 3
    ConditionalRoutingPage.setNumberOfRepeats(numberOfRepeats)
                          .submit()
                          .completeBlocks(numberOfRepeats)


    // Then
    expect(ConditionalRoutingPage.isBlock('summary')).to.be.true
  })

  it('Given two repeating groups, when I select yes for first question, I should be routed to the correct block.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)

    //When
    ConditionalRoutingPage.setNumberOfRepeats(2)
                          .submit()
                          .clickAgeAndShoeSize()
                          .submit()

    // Then
    expect(ConditionalRoutingPage.isGroup('0')).to.be.true
    expect(ConditionalRoutingPage.isBlock('age-block')).to.be.true
  })

  it('Given two repeating groups, when I select no for first question, I should be routed to the correct block.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)

    //When
    ConditionalRoutingPage.setNumberOfRepeats(2)
                          .submit()
                          .clickShoeSizeOnly()
                          .submit()

    // Then
    expect(ConditionalRoutingPage.isGroup('0')).to.be.true
    expect(ConditionalRoutingPage.isBlock('shoe-size-block')).to.be.true
  })

  it('Given two repeating groups, when I select yes for first question in the second group, I should be routed to the correct block.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)

    //When
    ConditionalRoutingPage.setNumberOfRepeats(2)
                          .submit()
                          .completeBlocks(1)
                          .clickAgeAndShoeSize()
                          .submit()

    // Then
    expect(ConditionalRoutingPage.isGroup('1')).to.be.true
    expect(ConditionalRoutingPage.isBlock('age-block')).to.be.true
  })

  it('Given two repeating groups, when I select no for first question in the second group, I should be routed to the correct block.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)

    //When
    ConditionalRoutingPage.setNumberOfRepeats(2)
                          .submit()
                          .completeBlocks(1)
                          .clickShoeSizeOnly()
                          .submit()

    // Then
    expect(ConditionalRoutingPage.isGroup('1')).to.be.true
    expect(ConditionalRoutingPage.isBlock('shoe-size-block')).to.be.true
  })

  it('Given three repeating groups, when I select yes for first question in the third group, I should be routed to the correct block.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)

    //When
    ConditionalRoutingPage.setNumberOfRepeats(3)
                          .submit()
                          .completeBlocks(2)
                          .clickAgeAndShoeSize()
                          .submit()

    // Then
    expect(ConditionalRoutingPage.isGroup('2')).to.be.true
    expect(ConditionalRoutingPage.isBlock('age-block')).to.be.true
  })

  it('Given three repeating groups, when I select no for first question in the third group, I should be routed to the correct block.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)

    //When
    ConditionalRoutingPage.setNumberOfRepeats(3)
                          .submit()
                          .completeBlocks(2)
                          .clickShoeSizeOnly()
                          .submit()

    // Then
    expect(ConditionalRoutingPage.isGroup('2')).to.be.true
    expect(ConditionalRoutingPage.isBlock('shoe-size-block')).to.be.true
  })

})
