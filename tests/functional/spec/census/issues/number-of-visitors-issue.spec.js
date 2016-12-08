import chai from 'chai'
import {startCensusQuestionnaire} from '../../../helpers'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'

const expect = chai.expect

describe('Number of visitors', function () {
  it('Given a census schema, When I dont enter any value for question: How many visitors are staying overnight here on 9th April 2017?, Then I should get an error message ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.submit()

    expect(OvernightVisitors.getErrorMsg()).to.equal('Please enter a value even if that value is 0')
  })
})
