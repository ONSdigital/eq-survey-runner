import {openQuestionnaire} from '../helpers'
import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page'
import HouseholdRelationshipPage from '../pages/surveys/relationship/relationships.page'
import SummaryPage from '../pages/summary.page'


describe('Household relationship', function() {



  it('Given I am on the household page when I enter Joe Bloggs then I should not have to enter relationship details', function() {
    // Given
    openQuestionnaire('test_relationship_household.json')
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')

    // When
    HouseholdCompositionPage.submit()

    // Then
    expect(SummaryPage.isOpen()).to.be.true
  })

  it('Given I answer the relationship questions for Joe Bloggs when answer the relationship questions for Jane Doe then I should not have to enter relationship details for John Doe', function() {
    // Given
    openQuestionnaire('test_relationship_household.json')
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
      .addPerson()
      .setPersonName(1, 'Jane Doe')
      .addPerson()
      .setPersonName(2, 'John Doe')
      .submit()
    HouseholdRelationshipPage.setWhoIsRelatedHusbandOrWife(0)
      .setWhoIsRelatedSonOrDaughter(1)
      .submit()

    // When
    HouseholdRelationshipPage.setWhoIsRelatedHusbandOrWife(0)
      .submit()

    // Then
    expect(SummaryPage.isOpen()).to.be.true
  })

  it('Given I answer the relationship questions for Joe Bloggs when I click previous on the Jane Doe relationship question then the relationships for John Bloggs should still be selected', function() {
    // Given
    openQuestionnaire('test_relationship_household.json')
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
      .addPerson()
      .setPersonName(1, 'Jane Doe')
      .addPerson()
      .setPersonName(2, 'John Doe')
      .submit()
    HouseholdRelationshipPage.setWhoIsRelatedHusbandOrWife(0)
      .setWhoIsRelatedSonOrDaughter(1)
      .submit()

    // When
    browser.back()

    // Then
    expect(browser.getValue('[name="who-is-related-0"]')).to.equal("Husband or wife")
    expect(browser.getValue('[name="who-is-related-1"]')).to.equal("Son or daughter")
  })


})
