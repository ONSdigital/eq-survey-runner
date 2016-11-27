import chai from 'chai'
import {startQuestionnaire, getBlockId, getRepeatedGroup} from '../helpers'
import AgePage from '../pages/surveys/repeating_groups/age.page.js'
import ShoeSizePage from '../pages/surveys/repeating_groups/shoe-size.page.js'
import AgeOrShoeSizePage from '../pages/surveys/repeating_groups/age-or-shoe-size.page.js'
import NumberOfRepeatsPage from '../pages/surveys/repeating_groups/number-of-repeats.page.js'
import SummaryPage from '../pages/summary.page.js'

const expect = chai.expect

describe('Repeating groups.', function() {

  var repeating_and_conditional_routing_schema = 'test_repeating_and_conditional_routing.json';

  it('Given a group of questions will repeat three times, when I complete the three groups of questions, then I should see a summary page of the questions.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)
    NumberOfRepeatsPage.setNumberOfRepeats(3)
                        .submit()

    //When
    completeBlocks(3)

    // Then
    expect(SummaryPage.isOpen()).to.be.true
  })

  it('Given a group of questions will repeat two times, when I select age and shoe size, then I should see a question for age.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)
    NumberOfRepeatsPage.setNumberOfRepeats(2)
                        .submit()

    //When
    AgeOrShoeSizePage.clickAgeAndShoeSize()
                      .submit()

    // Then
    expect(getRepeatedGroup()).to.equal('0')
    expect(getBlockId()).to.equal('age-block')
  })

  it('Given the number of repeats question has been set to two, when I select shoe size, then I should see a question for shoe size.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)
    NumberOfRepeatsPage.setNumberOfRepeats(2)
                        .submit()

    //When
    AgeOrShoeSizePage.clickShoeSizeOnly()
                      .submit()

    // Then
    expect(getRepeatedGroup()).to.equal('0')
    expect(getBlockId()).to.equal('shoe-size-block')
  })

  it('Given I have completed the questions to the first of two groups, when I select age and shoe size, then I should see a question for age.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)
    NumberOfRepeatsPage.setNumberOfRepeats(2)
                        .submit()
    completeBlocks(1)

    //When
    AgeOrShoeSizePage.clickAgeAndShoeSize()
                      .submit()

    // Then
    expect(getRepeatedGroup()).to.equal('1')
    expect(getBlockId()).to.equal('age-block')
  })

  it('Given I have completed the questions to the first of two groups, when I select shoe size, then I should see a question for shoe size.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)
    NumberOfRepeatsPage.setNumberOfRepeats(2)
                        .submit()
    completeBlocks(1)

    //When
    AgeOrShoeSizePage.clickShoeSizeOnly()
                      .submit()

    // Then
    expect(getRepeatedGroup()).to.equal('1')
    expect(getBlockId()).to.equal('shoe-size-block')
  })

  it('Given I am on the second question in the second group, when I go to the previous page, then I should see the first question for second group.', function() {
    //Given
    startQuestionnaire(repeating_and_conditional_routing_schema)
    NumberOfRepeatsPage.setNumberOfRepeats(2)
                        .submit()
    completeBlocks(1)
    AgeOrShoeSizePage.clickAgeAndShoeSize()
                      .submit()
    AgePage.setAge(15)
            .submit()

    //When
    ShoeSizePage.previous()

    // Then
    expect(getRepeatedGroup()).to.equal('1')
    expect(getBlockId()).to.equal('age-block')
  })

})

function completeBlocks(numberToComplete) {
   var i
   for (var i = 0; i < numberToComplete; i++) {
      AgeOrShoeSizePage.clickAgeAndShoeSize(1).submit()
      AgePage.setAge(15).submit()
      ShoeSizePage.setShoeSize(3).submit()
   }
}
