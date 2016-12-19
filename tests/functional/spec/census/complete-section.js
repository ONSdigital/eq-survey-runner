import TypeOfAccommodation from '../../pages/surveys/census/household/type-of-accommodation.page.js'
import TypeOfHouse from '../../pages/surveys/census/household/type-of-house.page.js'
import SelfContainedAccommodation from '../../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../../pages/surveys/census/household/central-heating.page.js'
import OwnOrRent from '../../pages/surveys/census/household/own-or-rent.page.js'
import NumberOfVehicles from '../../pages/surveys/census/household/number-of-vehicles.page.js'
import HouseholdAndAccommodationCompleted from '../../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import HouseholdMemberBegin from '../../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../../pages/surveys/census/household/details-correct.page.js'
import Over16 from '../../pages/surveys/census/household/over-16.page.js'
import PrivateResponse from '../../pages/surveys/census/household/private-response.page.js'
import Sex from '../../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../../pages/surveys/census/household/date-of-birth.page.js'
import MaritalStatus from '../../pages/surveys/census/household/marital-status.page.js'
import AnotherAddress from '../../pages/surveys/census/household/another-address.page.js'
import InEducation from '../../pages/surveys/census/household/in-education.page.js'
import CountryOfBirth from '../../pages/surveys/census/household/country-of-birth.page.js'
import Carer from '../../pages/surveys/census/household/carer.page.js'
import NationalIdentity from '../../pages/surveys/census/household/national-identity.page.js'
import EthnicGroup from '../../pages/surveys/census/household/ethnic-group.page.js'
import WhiteEthnicGroup from '../../pages/surveys/census/household/white-ethnic-group.page.js'
import Language from '../../pages/surveys/census/household/language.page.js'
import Religion from '../../pages/surveys/census/household/religion.page.js'
import PastUsualAddress from '../../pages/surveys/census/household/past-usual-address.page.js'
import Passports from '../../pages/surveys/census/household/passports.page.js'
import Disability from '../../pages/surveys/census/household/disability.page.js'
import Qualifications from '../../pages/surveys/census/household/qualifications.page.js'
import Volunteering from '../../pages/surveys/census/household/volunteering.page.js'
import EmploymentType from '../../pages/surveys/census/household/employment-type.page.js'
import Jobseeker from '../../pages/surveys/census/household/jobseeker.page.js'
import JobAvailability from '../../pages/surveys/census/household/job-availability.page.js'
import JobPending from '../../pages/surveys/census/household/job-pending.page.js'
import Occupation from '../../pages/surveys/census/household/occupation.page.js'
import EverWorked from '../../pages/surveys/census/household/ever-worked.page.js'
import MainJob from '../../pages/surveys/census/household/main-job.page.js'
import JobTitle from '../../pages/surveys/census/household/job-title.page.js'
import JobDescription from '../../pages/surveys/census/household/job-description.page.js'
import EmployersBusiness from '../../pages/surveys/census/household/employers-business.page.js'
import MainJobType from '../../pages/surveys/census/household/main-job-type.page.js'
import BusinessName from '../../pages/surveys/census/household/business-name.page.js'
import HouseholdMemberCompleted from '../../pages/surveys/census/household/household-member-completed.page.js'
import VisitorBegin from '../../pages/surveys/census/household/visitor-begin.page.js'
import VisitorName from '../../pages/surveys/census/household/visitor-name.page.js'
import VisitorSex from '../../pages/surveys/census/household/visitor-sex.page.js'
import VisitorDateOfBirth from '../../pages/surveys/census/household/visitor-date-of-birth.page.js'
import VisitorUkResident from '../../pages/surveys/census/household/visitor-uk-resident.page.js'
import VisitorAddress from '../../pages/surveys/census/household/visitor-address.page.js'
import VisitorCompleted from '../../pages/surveys/census/household/visitor-completed.page.js'

export const completeHouseholdAndAccommodation = () => {
  TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
  TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
  SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
  NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
  CentralHeating.clickCentralHeatingAnswerGas().submit()
  OwnOrRent.clickOwnOrRentAnswerOwnsOutright().submit()
  NumberOfVehicles.setNumberOfVehiclesAnswer(2).submit()
  HouseholdAndAccommodationCompleted.submit()
}

export const completeVisitorSection = () => {
  VisitorBegin.submit()
  VisitorName.setVisitorFirstName('Jane').setVisitorLastName('Doe').submit()
  VisitorSex.clickVisitorSexAnswerFemale().submit()
  VisitorDateOfBirth.setVisitorDateOfBirthAnswerDay(10).setVisitorDateOfBirthAnswerMonth(7).setVisitorDateOfBirthAnswerYear(1990).submit()
  VisitorUkResident.clickVisitorUkResidentAnswerYesUsuallyLivesInTheUnitedKingdom().submit()
  VisitorAddress.setVisitorAddressAnswerBuilding(50).setVisitorAddressAnswerStreet('My Road').setVisitorAddressAnswerCity('Newport').setVisitorAddressAnswerPostcode('AB123CD').submit()
  VisitorCompleted.submit()
}

export const completeHouseholdDetails = () => {
  HouseholdMemberBegin.submit()
  DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
  Over16.clickOver16AnswerYes().submit()
  PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
  Sex.clickSexAnswerMale().submit()
  DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
  MaritalStatus.clickMaritalStatusAnswerMarried().submit()
  AnotherAddress.clickAnotherAddressAnswerNo().submit()
  InEducation.clickInEducationAnswerNo().submit()
  CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
  Carer.clickCarerAnswerNo().submit()
  NationalIdentity.clickNationalIdentityEnglandAnswerEnglish().submit()
  EthnicGroup.clickEthnicGroupEnglandAnswerWhite().submit()
  WhiteEthnicGroup.clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish().submit()
  Language.clickLanguageEnglandAnswerEnglish().submit()
  Religion.clickReligionAnswerNoReligion().submit()
  PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
  Passports.clickPassportsAnswerUnitedKingdom().submit()
  Disability.clickDisabilityAnswerNo().submit()
  Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
  Volunteering.clickVolunteeringAnswerNo().submit()
  EmploymentType.clickEmploymentTypeAnswerNoneOfTheAbove().submit()
  Jobseeker.clickJobseekerAnswerYes().submit()
  JobAvailability.clickJobAvailabilityAnswerYes().submit()
  JobPending.clickJobPendingAnswerNo().submit()
  Occupation.clickOccupationAnswerAStudent().submit()
  EverWorked.clickEverWorkedAnswerYes().submit()
  MainJob.clickMainJobAnswerAnEmployee().submit()
  JobTitle.setJobTitleAnswer('Dev').submit()
  JobDescription.setJobDescriptionAnswer('writing lots of code').submit()
  EmployersBusiness.setEmployersBusinessAnswer('something statistical').submit()
  MainJobType.clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness().submit()
  BusinessName.setBusinessNameAnswer('ONS').submit()
  HouseholdMemberCompleted.submit()
}
