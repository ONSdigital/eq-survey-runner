import chai from 'chai'
import {startCensusQuestionnaire} from '../../../helpers'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import ElsePermanentOrFamilyHome from '../../../pages/surveys/census/household/else-permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'
import WhoLivesHereCompleted from '../../../pages/surveys/census/household/who-lives-here-completed.page.js'
import TypeOfAccommodation from '../../../pages/surveys/census/household/type-of-accommodation.page.js'
import TypeOfHouse from '../../../pages/surveys/census/household/type-of-house.page.js'
import SelfContainedAccommodation from '../../../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../../../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../../../pages/surveys/census/household/central-heating.page.js'
import HouseholdAndAccommodationCompleted from '../../../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import VisitorBegin from '../../../pages/surveys/census/household/visitor-begin.page.js'

const expect = chai.expect

describe('Census routing Scenarios', function () {

  it('Given I have added a person in my household, When I change my mind and they should be visitors, Then I do not have to answer household member details', function () {
    startCensusQuestionnaire('census_household.json')

    // Given
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').submit()
    EveryoneAtAddressConfirmation.previous()
    HouseholdComposition.previous()
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
    ElsePermanentOrFamilyHome.clickElsePermanentOrFamilyHomeAnswerNoOneLivesHereAsTheirPermanentHome().submit()

    // When
    OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
    WhoLivesHereCompleted.submit()
    TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
    TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
    SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
    NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
    CentralHeating.clickCentralHeatingAnswerGas().submit()
    HouseholdAndAccommodationCompleted.submit()

    // Then
    expect(VisitorBegin.isOpen()).to.equal(true, 'Expected to skip household details')
  })

})
