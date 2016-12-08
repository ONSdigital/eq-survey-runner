import chai from 'chai'
import {startQuestionnaire, getBlockId, getRepeatedGroup} from '../helpers'
import AgePage from '../pages/surveys/repeating_groups/age.page.js'
import ShoeSizePage from '../pages/surveys/repeating_groups/shoe-size.page.js'
import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page.js'
import RepeatingHouseholdPage from '../pages/surveys/repeating_household/repeating-household.page.js'
import SummaryPage from '../pages/summary.page.js'

const expect = chai.expect

describe('Populating household names on subsequent repeating groups.', function() {

  var repeating_household_schema = 'test_repeating_household.json';

  it('Given I enter one name, when I navigate through the subsequent group, I should see the name on each block.', function() {
    // Given
    startQuestionnaire(repeating_household_schema)
    var name = 'Person One'

    // When
    HouseholdCompositionPage.setPersonName(0, name).submit()

    expect(RepeatingHouseholdPage.getDisplayedName()).to.contain(name)
    AgePage.setAge(99).submit()
    expect(RepeatingHouseholdPage.getDisplayedName()).to.contain(name)
  })

  it('Given I enter multiple names, when I navigate through the subsequent groups, I should the names on their respective blocks.', function() {
    // Given
    startQuestionnaire(repeating_household_schema)
    var name1 = 'Person One'
    var name2 = 'Person Two'
    var name3 = 'Person Three'

    // When
    HouseholdCompositionPage
        .setPersonName(0, name1)
        .addPerson()
        .setPersonName(1, name2)
        .addPerson()
        .setPersonName(2, name3)
        .submit()

    // Person One
    expect(RepeatingHouseholdPage.getDisplayedName()).to.contain(name1)
    AgePage.setAge(99).submit()
    expect(RepeatingHouseholdPage.getDisplayedName()).to.contain(name1)
    ShoeSizePage.setShoeSize(10).submit()

    // Person Two
    expect(RepeatingHouseholdPage.getDisplayedName()).to.contain(name2)
    AgePage.setAge(99).submit()
    expect(RepeatingHouseholdPage.getDisplayedName()).to.contain(name2)
    ShoeSizePage.setShoeSize(10).submit()

    // Person Three
    expect(RepeatingHouseholdPage.getDisplayedName()).to.contain(name3)
    AgePage.setAge(99).submit()
    expect(RepeatingHouseholdPage.getDisplayedName()).to.contain(name3)
    ShoeSizePage.setShoeSize(10).submit()

  })

})
