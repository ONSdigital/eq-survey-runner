import {startCensusQuestionnaire} from '../../../helpers'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'
import HouseholdRelationships from '../../../pages/surveys/census/household/household-relationships.page.js'
import WhoLivesHereCompleted from '../../../pages/surveys/census/household/who-lives-here-completed.page.js'
import TypeOfAccommodation from '../../../pages/surveys/census/household/type-of-accommodation.page.js'
import TypeOfHouse from '../../../pages/surveys/census/household/type-of-house.page.js'
import SelfContainedAccommodation from '../../../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../../../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../../../pages/surveys/census/household/central-heating.page.js'
import OwnOrRent from '../../../pages/surveys/census/household/own-or-rent.page.js'
import NumberOfVehicles from '../../../pages/surveys/census/household/number-of-vehicles.page.js'
import HouseholdAndAccommodationCompleted from '../../../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import HouseholdMemberBegin from '../../../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../../../pages/surveys/census/household/details-correct.page.js'
import Sex from '../../../pages/surveys/census/household/sex.page.js'

describe('Individual section Question 1', function () {

  it('Given I am answering question 1 in the individual detail section, When I do not select any response, Then I am routed to What is you sex question 2 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    HouseholdRelationships.clickHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

  // household-and-accommodation
    TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
    TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
    SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
    NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
    CentralHeating.clickCentralHeatingAnswerGas().submit()
    OwnOrRent.clickOwnOrRentAnswerOwnsOutright().submit()
    NumberOfVehicles.setNumberOfVehiclesAnswer(2).submit()
    HouseholdAndAccommodationCompleted.submit()

  // household-member
    HouseholdMemberBegin.submit()
    DetailsCorrect.submit()
    Sex.clickSexAnswerMale().submit()
  })

})
