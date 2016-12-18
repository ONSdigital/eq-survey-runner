import chai from 'chai'
import {startCensusQuestionnaire} from '../../../helpers'
import {completeHouseholdAndAccommodation, completeVisitorSection, completeHouseholdDetails} from '../complete-section'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import ElsePermanentOrFamilyHome from '../../../pages/surveys/census/household/else-permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'
import HouseholdRelationships from '../../../pages/surveys/census/household/household-relationships.page.js'
import WhoLivesHereCompleted from '../../../pages/surveys/census/household/who-lives-here-completed.page.js'
import TypeOfAccommodation from '../../../pages/surveys/census/household/type-of-accommodation.page.js'
import TypeOfHouse from '../../../pages/surveys/census/household/type-of-house.page.js'
import TypeOfFlat from '../../../pages/surveys/census/household/type-of-flat.page.js'
import SelfContainedAccommodation from '../../../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../../../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../../../pages/surveys/census/household/central-heating.page.js'
import OwnOrRent from '../../../pages/surveys/census/household/own-or-rent.page.js'
import Landlord from '../../../pages/surveys/census/household/landlord.page.js'
import NumberOfVehicles from '../../../pages/surveys/census/household/number-of-vehicles.page.js'
import HouseholdAndAccommodationCompleted from '../../../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import HouseholdMemberBegin from '../../../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../../../pages/surveys/census/household/details-correct.page.js'
import CorrectName from '../../../pages/surveys/census/household/correct-name.page.js'
import Over16 from '../../../pages/surveys/census/household/over-16.page.js'
import PrivateResponse from '../../../pages/surveys/census/household/private-response.page.js'
import RequestPrivateResponse from '../../../pages/surveys/census/household/request-private-response.page.js'
import Sex from '../../../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../../../pages/surveys/census/household/date-of-birth.page.js'
import MaritalStatus from '../../../pages/surveys/census/household/marital-status.page.js'
import AnotherAddress from '../../../pages/surveys/census/household/another-address.page.js'
import OtherAddress from '../../../pages/surveys/census/household/other-address.page.js'
import AddressType from '../../../pages/surveys/census/household/address-type.page.js'
import InEducation from '../../../pages/surveys/census/household/in-education.page.js'
import TermTimeLocation from '../../../pages/surveys/census/household/term-time-location.page.js'
import CountryOfBirth from '../../../pages/surveys/census/household/country-of-birth.page.js'
import ArriveInUk from '../../../pages/surveys/census/household/arrive-in-uk.page.js'
import LengthOfStay from '../../../pages/surveys/census/household/length-of-stay.page.js'
import Carer from '../../../pages/surveys/census/household/carer.page.js'
import NationalIdentity from '../../../pages/surveys/census/household/national-identity.page.js'
import EthnicGroup from '../../../pages/surveys/census/household/ethnic-group.page.js'
import WhiteEthnicGroup from '../../../pages/surveys/census/household/white-ethnic-group.page.js'
import MixedEthnicGroup from '../../../pages/surveys/census/household/mixed-ethnic-group.page.js'
import AsianEthnicGroup from '../../../pages/surveys/census/household/asian-ethnic-group.page.js'
import BlackEthnicGroup from '../../../pages/surveys/census/household/black-ethnic-group.page.js'
import OtherEthnicGroup from '../../../pages/surveys/census/household/other-ethnic-group.page.js'
import SexualIdentity from '../../../pages/surveys/census/household/sexual-identity.page.js'
import UnderstandWelsh from '../../../pages/surveys/census/household/understand-welsh.page.js'
import Language from '../../../pages/surveys/census/household/language.page.js'
import English from '../../../pages/surveys/census/household/english.page.js'
import Religion from '../../../pages/surveys/census/household/religion.page.js'
import PastUsualAddress from '../../../pages/surveys/census/household/past-usual-address.page.js'
import Passports from '../../../pages/surveys/census/household/passports.page.js'
import Disability from '../../../pages/surveys/census/household/disability.page.js'
import Qualifications from '../../../pages/surveys/census/household/qualifications.page.js'
import Volunteering from '../../../pages/surveys/census/household/volunteering.page.js'
import EmploymentType from '../../../pages/surveys/census/household/employment-type.page.js'
import Jobseeker from '../../../pages/surveys/census/household/jobseeker.page.js'
import JobAvailability from '../../../pages/surveys/census/household/job-availability.page.js'
import JobPending from '../../../pages/surveys/census/household/job-pending.page.js'
import Occupation from '../../../pages/surveys/census/household/occupation.page.js'
import EverWorked from '../../../pages/surveys/census/household/ever-worked.page.js'
import MainJob from '../../../pages/surveys/census/household/main-job.page.js'
import JobTitle from '../../../pages/surveys/census/household/job-title.page.js'
import JobDescription from '../../../pages/surveys/census/household/job-description.page.js'
import EmployersBusiness from '../../../pages/surveys/census/household/employers-business.page.js'
import MainJobType from '../../../pages/surveys/census/household/main-job-type.page.js'
import BusinessName from '../../../pages/surveys/census/household/business-name.page.js'
import HouseholdMemberCompleted from '../../../pages/surveys/census/household/household-member-completed.page.js'
import VisitorBegin from '../../../pages/surveys/census/household/visitor-begin.page.js'
import VisitorName from '../../../pages/surveys/census/household/visitor-name.page.js'
import VisitorSex from '../../../pages/surveys/census/household/visitor-sex.page.js'
import VisitorDateOfBirth from '../../../pages/surveys/census/household/visitor-date-of-birth.page.js'
import VisitorUkResident from '../../../pages/surveys/census/household/visitor-uk-resident.page.js'
import VisitorAddress from '../../../pages/surveys/census/household/visitor-address.page.js'
import VisitorCompleted from '../../../pages/surveys/census/household/visitor-completed.page.js'
import VisitorsCompleted from '../../../pages/surveys/census/household/visitors-completed.page.js'
import Confirmation from '../../../pages/confirmation.page.js'
import ThankYou from '../../../pages/thank-you.page'

const expect = chai.expect

describe('Who lives here routing Scenarios', function () {

  it('Given I am answering question 1 in the who lives here section, When I select -yes- as the response, Then I am routed to Who lives here question 2 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    expect(HouseholdComposition.isOpen()).to.equal(true, 'Expecting go to household composition')
  })

  it('Given I am answering question 1 in the who lives here section, When I select -no- as the response, Then I am routed to Who lives here question 1a Can you confirm no one lives here', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
    expect(ElsePermanentOrFamilyHome.isOpen()).to.equal(true, 'Expecting go to else permanent or family home')
  })

  it('Given I am answering question 1 in the who lives here section, When I dont select any response, Then I a alert msg saying mandatory field must be displayed ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.submit()
    expect(PermanentOrFamilyHome.getAlertText()).to.contain('Please select an answer to continue')
  })

  it('Given I am answering question 1a in the who lives here section, When I select -yes- as the response, Then I am routed to Who lives here question 2 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
    ElsePermanentOrFamilyHome.clickElsePermanentOrFamilyHomeAnswerSomeoneLivesHereAsTheirPermanentHome().submit()
    expect(HouseholdComposition.isOpen()).to.equal(true, 'Expecting go to household composition')
  })

  it('Given I am answering question 1a in the who lives here section, When I select -no- as the response, Then I am routed to How many visitors... question 4 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
    ElsePermanentOrFamilyHome.clickElsePermanentOrFamilyHomeAnswerNoOneLivesHereAsTheirPermanentHome().submit()
    expect(OvernightVisitors.isOpen()).to.equal(true, 'Expecting go to overnight visitors')
  })

  it('Given I am answering question 1a in the who lives here section, When I select -no- as the response, Then I am routed to How many visitors... question 4 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
    ElsePermanentOrFamilyHome.submit()
    expect(ElsePermanentOrFamilyHome.getAlertText()).to.contain('Please select an answer to continue')
  })

  it('Given I am answering question 3 in the who lives here section, When I select -yes- as the response, Then I am routed to Who lives here question 4 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    expect(OvernightVisitors.isOpen()).to.equal(true, 'Expecting go to overnight visitors')
  })

  it('Given I am answering question 3 in the who lives here section, When I select -no- as the response, Then I am routed back to Who lives here question 2 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerNoINeedToAddAnotherPerson().submit()
    expect(HouseholdComposition.isOpen()).to.equal(true, 'Expecting go to household composition')
  })

  // issue present - displaying on screen validation error which is not in spec
  it('Given I am answering question 3 in the who lives here section, When I dont select any response, Then I am routed to Who lives here question 4 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.submit()
    expect(OvernightVisitors.isOpen()).to.equal(true, 'Expecting go to overnight visitors')
  })

  it('Given I am answering question 1 in the individual detail section, When I select -yes- as response, Then I am routed to Are you over 16 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
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
    DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
    Over16.clickOver16AnswerYes().submit()
  })

  it('Given I am answering question 1 in the individual detail section, When I select -no- as response, Then I am routed to What is your correct name question 1a ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
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
    DetailsCorrect.clickDetailsCorrectAnswerNoINeedToChangeMyName().submit()
    CorrectName.setCorrectFirstName('Yoganand Kumar Kunche').submit()
  })

  it('Given I am answering question 1 in the individual detail section, When I do not select any response, Then I am routed to Are you over 16', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
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
    Over16.clickOver16AnswerYes().submit()
  })

    it('Given two people are in the household, When I complete the household details for person one, Then I should be asked household details for person two.', function () {
    startCensusQuestionnaire('census_household.json')

    // Given
    // who-lives-here
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
    HouseholdRelationships.clickHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

    // household-and-accommodation
    completeHouseholdAndAccommodation()

    // When
    // household-member
    completeHouseholdDetails()

    // Then
    expect(HouseholdMemberBegin.isOpen()).to.equal(true, 'Expected be on the household member details for person two')
  })

  it('Given I do not enter a first name, When I save and continue, Then I should see errors that suggests first name is mandatory.', function () {
    startCensusQuestionnaire('census_household.json', false, 'GB-WLS')

    // who-lives-here
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.submit()

    expect(HouseholdComposition.getErrorMsg()).to.contain('Please enter a name or remove the person to continue')
  })

  it('Given I enter a first name but no middle or surname, When I save and continue, Then I should not see any errors', function () {
    startCensusQuestionnaire('census_household.json', false, 'GB-WLS')

    // who-lives-here
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').submit()
    expect(EveryoneAtAddressConfirmation.isOpen()).to.be.true
  })

})
