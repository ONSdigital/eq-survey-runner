import {startCensusQuestionnaire} from '../../../helpers'
import {completeHouseholdAndAccommodation} from '../complete-section'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'
import HouseholdRelationships from '../../../pages/surveys/census/household/household-relationships.page.js'
import WhoLivesHereCompleted from '../../../pages/surveys/census/household/who-lives-here-completed.page.js'
import HouseholdMemberBegin from '../../../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../../../pages/surveys/census/household/details-correct.page.js'
import Over16 from '../../../pages/surveys/census/household/over-16.page.js'
import PrivateResponse from '../../../pages/surveys/census/household/private-response.page.js'
import Sex from '../../../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../../../pages/surveys/census/household/date-of-birth.page.js'
import MaritalStatus from '../../../pages/surveys/census/household/marital-status.page.js'
import AnotherAddress from '../../../pages/surveys/census/household/another-address.page.js'
import InEducation from '../../../pages/surveys/census/household/in-education.page.js'
import CountryOfBirth from '../../../pages/surveys/census/household/country-of-birth.page.js'
import Carer from '../../../pages/surveys/census/household/carer.page.js'
import NationalIdentity from '../../../pages/surveys/census/household/national-identity.page.js'
import EthnicGroup from '../../../pages/surveys/census/household/ethnic-group.page.js'
import BlackEthnicGroup from '../../../pages/surveys/census/household/black-ethnic-group.page.js'
import Language from '../../../pages/surveys/census/household/language.page.js'
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
import HouseholdMemberCompleted from '../../../pages/surveys/census/household/household-member-completed.page.js'


describe('Ever worked routing Scenarios', function () {

  it('Given I am answering question 33 Have you ever worked?, When I answer No, Then i am routed to end end of the person', function () {
    startCensusQuestionnaire('census_household.json', false)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    HouseholdRelationships.setHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

    // household-and-accommodation
    completeHouseholdAndAccommodation()

    // household-member
    HouseholdMemberBegin.submit()
    DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
    Over16.clickOver16AnswerYes().submit()
    PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerWales().submit()
    Carer.clickCarerAnswerNo().submit()
    NationalIdentity.clickNationalIdentityEnglandAnswerWelsh().submit()
    EthnicGroup.clickEthnicGroupEnglandAnswerBlackAfricanCaribbeanBlackBritish().submit()
    BlackEthnicGroup.clickBlackEthnicGroupAnswerAfrican().submit()
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
    EverWorked.clickEverWorkedAnswerNo().submit()

    expect(HouseholdMemberCompleted.isOpen()).to.equal(true, 'Expecting go to HouseholdMemberCompleted')
  })

  it('Given I am answering question 33 Have you ever worked?, When I dont answer, Then i am routed to end end of the person', function () {
    startCensusQuestionnaire('census_household.json', false)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    HouseholdRelationships.setHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

    // household-and-accommodation
    completeHouseholdAndAccommodation()

    // household-member
    HouseholdMemberBegin.submit()
    DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
    Over16.clickOver16AnswerYes().submit()
    PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerWales().submit()
    Carer.clickCarerAnswerNo().submit()
    NationalIdentity.clickNationalIdentityEnglandAnswerWelsh().submit()
    EthnicGroup.clickEthnicGroupEnglandAnswerBlackAfricanCaribbeanBlackBritish().submit()
    BlackEthnicGroup.clickBlackEthnicGroupAnswerAfrican().submit()
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
    EverWorked.submit()

    expect(HouseholdMemberCompleted.isOpen()).to.equal(true, 'Expecting go to HouseholdMemberCompleted')
  })

  it('Given I am answering question 33 Have you ever worked?, When I answer yes, Then i am routed to main job question', function () {
    startCensusQuestionnaire('census_household.json', false)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
    EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    HouseholdRelationships.setHouseholdRelationshipsAnswerHusbandOrWife().submit()
    WhoLivesHereCompleted.submit()

    // household-and-accommodation
    completeHouseholdAndAccommodation()

    // household-member
    HouseholdMemberBegin.submit()
    DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
    Over16.clickOver16AnswerYes().submit()
    PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerWales().submit()
    Carer.clickCarerAnswerNo().submit()
    NationalIdentity.clickNationalIdentityEnglandAnswerWelsh().submit()
    EthnicGroup.clickEthnicGroupEnglandAnswerBlackAfricanCaribbeanBlackBritish().submit()
    BlackEthnicGroup.clickBlackEthnicGroupAnswerAfrican().submit()
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

    expect(MainJob.isOpen()).to.equal(true, 'Expecting go to MainJob')
  })

})
