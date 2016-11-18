import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page'
import HouseholdRelationshipPage from '../pages/surveys/relationship/household-relationship.page'

const expect = chai.expect

describe('Household relationship', function() {

   var schema = 'test_household_relationship.json'

   it('Given I have added Joe Bloggs, Jane Doe and John Doe to my household when I am on the relationships page then I should see the questions `Joe Bloggs is the ... of Jane Doe` and `Joe Bloggs is the ... of John Doe`', function() {
      // Given
      startQuestionnaire(schema)
      HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
         .addPerson()
         .setPersonName(1, 'Jane Doe')
         .addPerson()
         .setPersonName(2, 'John Doe')

      // When
      HouseholdCompositionPage.submit()

      // Then
      expect(HouseholdRelationshipPage.getRelationshipLabelAt(0)).to.have.string('Joe Bloggs is the ... of Jane Doe')
      expect(HouseholdRelationshipPage.getRelationshipLabelAt(1)).to.have.string('Joe Bloggs is the ... of John Doe');
  })

   it('Given I have answered how Joe Bloggs is related Jane Doe and John Doe when I go to the next relationship question then I should see the questions `Jane Doe is the ... of Joe Bloggs`, `Jane Doe is the ... of John Doe`', function() {
      // Given
      startQuestionnaire(schema)
      HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
         .addPerson()
         .setPersonName(1, 'Jane Doe')
         .addPerson()
         .setPersonName(2, 'John Doe')
         .submit()

      // When
      HouseholdRelationshipPage.setFatherRelationship(0)
         .setSonRelationship(1)
         .submit()

      // Then
      expect(HouseholdRelationshipPage.getRelationshipLabelAt(0)).to.have.string('Jane Doe is the ... of Joe Bloggs')
      expect(HouseholdRelationshipPage.getRelationshipLabelAt(1)).to.have.string('Jane Doe is the ... of John Doe')
   })

   it('Given I have added Joe Bloggs, Jane Doe and John Doe to my household when I am on the relationships page then I should see the title `Describe how Joe Bloggs is related to the others`', function() {
      // Given
      startQuestionnaire(schema)
      HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
         .addPerson()
         .setPersonName(1, 'Jane Doe')
         .addPerson()
         .setPersonName(2, 'John Doe')

      // When
      HouseholdCompositionPage.submit()

      // Then
      expect(HouseholdRelationshipPage.getQuestionTitle()).to.have.string('Describe how Joe Bloggs is related to the others')
   })

})
