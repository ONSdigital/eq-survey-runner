import chai from 'chai'
import {startCensusQuestionnaire} from '../helpers'

import CorrectName from '../pages/surveys/census/individual/correct-name.page.js'
import Sex from '../pages/surveys/census/individual/sex.page.js'
import DateOfBirth from '../pages/surveys/census/individual/date-of-birth.page.js'
import MaritalStatus from '../pages/surveys/census/individual/marital-status.page.js'
import AnotherAddress from '../pages/surveys/census/individual/another-address.page.js'
import OtherAddress from '../pages/surveys/census/individual/other-address.page.js'
import AddressType from '../pages/surveys/census/individual/address-type.page.js'
import InEducation from '../pages/surveys/census/individual/in-education.page.js'
import TermTimeLocation from '../pages/surveys/census/individual/term-time-location.page.js'
import CountryOfBirth from '../pages/surveys/census/individual/country-of-birth.page.js'
import ArriveInUk from '../pages/surveys/census/individual/arrive-in-uk.page.js'
import LengthOfStay from '../pages/surveys/census/individual/length-of-stay.page.js'
import Carer from '../pages/surveys/census/individual/carer.page.js'
import NationalIdentity from '../pages/surveys/census/individual/national-identity.page.js'
import EthnicGroup from '../pages/surveys/census/individual/ethnic-group.page.js'
import WhiteEthnicGroup from '../pages/surveys/census/individual/white-ethnic-group.page.js'
import MixedEthnicGroup from '../pages/surveys/census/individual/mixed-ethnic-group.page.js'
import AsianEthnicGroup from '../pages/surveys/census/individual/asian-ethnic-group.page.js'
import BlackEthnicGroup from '../pages/surveys/census/individual/black-ethnic-group.page.js'
import OtherEthnicGroup from '../pages/surveys/census/individual/other-ethnic-group.page.js'
import SexualIdentity from '../pages/surveys/census/individual/sexual-identity.page.js'
import UnderstandWelsh from '../pages/surveys/census/individual/understand-welsh.page.js'
import Language from '../pages/surveys/census/individual/language.page.js'
import English from '../pages/surveys/census/individual/english.page.js'
import Religion from '../pages/surveys/census/individual/religion.page.js'
import PastUsualAddress from '../pages/surveys/census/individual/past-usual-address.page.js'
import LastYearAddress from '../pages/surveys/census/individual/last-year-address.page.js'
import Passports from '../pages/surveys/census/individual/passports.page.js'
import OtherPassports from '../pages/surveys/census/individual/other-passports.page.js'
import Disability from '../pages/surveys/census/individual/disability.page.js'
import Qualifications from '../pages/surveys/census/individual/qualifications.page.js'
import Volunteering from '../pages/surveys/census/individual/volunteering.page.js'
import EmploymentType from '../pages/surveys/census/individual/employment-type.page.js'
import Jobseeker from '../pages/surveys/census/individual/jobseeker.page.js'
import JobAvailability from '../pages/surveys/census/individual/job-availability.page.js'
import JobPending from '../pages/surveys/census/individual/job-pending.page.js'
import Occupation from '../pages/surveys/census/individual/occupation.page.js'
import EverWorked from '../pages/surveys/census/individual/ever-worked.page.js'
import MainJob from '../pages/surveys/census/individual/main-job.page.js'
import JobTitle from '../pages/surveys/census/individual/job-title.page.js'
import JobDescription from '../pages/surveys/census/individual/job-description.page.js'
import EmployersBusiness from '../pages/surveys/census/individual/employers-business.page.js'
import MainJobType from '../pages/surveys/census/individual/main-job-type.page.js'
import BusinessName from '../pages/surveys/census/individual/business-name.page.js'
import Confirmation from '../pages/surveys/census/individual/confirmation.page.js'
import ThankYou from '../pages/thank-you.page'

const expect = chai.expect

describe('Census Individual', function () {

    it('Given Respondent Home has identified the respondent should have the Individual Questionnaire without the sexual id question, When I complete the EQ, Then I should not be asked the sexual id question', function () {
        startCensusQuestionnaire('census_individual.json')

        // household-member
        CorrectName.setFirstName("Paul").setLastName("Smith").submit()
        Sex.clickSexAnswerMale().submit()
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(8).setDateOfBirthAnswerYear(1980).submit()
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        InEducation.clickInEducationAnswerNo().submit()
        CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
        Carer.clickCarerAnswerNo().submit()
        NationalIdentity.clickNationalIdentityEnglandAnswerBritish().submit()
        EthnicGroup.clickEthnicGroupEnglandAnswerWhite().submit()
        WhiteEthnicGroup.clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish().submit()
        Language.clickLanguageEnglandAnswerEnglish().submit()
        Religion.clickReligionAnswerNoReligion().submit()
        PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
        Passports.clickPassportsAnswerUnitedKingdom().submit()
        Disability.clickDisabilityAnswerNo().submit()
        Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
        Volunteering.clickVolunteeringAnswerNo().submit()
        EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().submit()
        MainJob.clickMainJobAnswerAnEmployee().submit()
        JobTitle.setJobTitleAnswer('dev').submit()
        JobDescription.setJobDescriptionAnswer('coding wizardry').submit()
        EmployersBusiness.setEmployersBusinessAnswer('codezilla').submit()
        MainJobType.clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness().submit()
        BusinessName.setBusinessNameAnswer('coding warehouse').submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true

    })

    it('Given Respondent Home has identified the respondent should have the Individual Questionnaire with the sexual id question, When I complete the EQ, Then I should be asked the sexual id question', function () {
        startCensusQuestionnaire('census_individual.json', true)

        // household-member
        CorrectName.setFirstName("Paul").setLastName("Smith").submit()
        Sex.clickSexAnswerMale().submit()
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(9).setDateOfBirthAnswerYear(1980).submit()
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        InEducation.clickInEducationAnswerNo().submit()
        CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
        Carer.clickCarerAnswerNo().submit()
        NationalIdentity.clickNationalIdentityEnglandAnswerBritish().submit()
        EthnicGroup.clickEthnicGroupEnglandAnswerWhite().submit()
        WhiteEthnicGroup.clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish().submit()
        SexualIdentity.clickSexualIdentityAnswerHeterosexualOrStraight().submit()
        Language.clickLanguageEnglandAnswerEnglish().submit()
        Religion.clickReligionAnswerNoReligion().submit()
        PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
        Passports.clickPassportsAnswerUnitedKingdom().submit()
        Disability.clickDisabilityAnswerNo().submit()
        Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
        Volunteering.clickVolunteeringAnswerNo().submit()
        EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().submit()
        MainJob.clickMainJobAnswerAnEmployee().submit()
        JobTitle.setJobTitleAnswer('dev').submit()
        JobDescription.setJobDescriptionAnswer('coding wizardry').submit()
        EmployersBusiness.setEmployersBusinessAnswer('codezilla').submit()
        MainJobType.clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness().submit()
        BusinessName.setBusinessNameAnswer('coding warehouse').submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true

    })

    it('Given the census theme is selected, then the help should not be visible', function() {
        // Given
        startCensusQuestionnaire('census_individual.json')
        // Then
        expect(browser.isVisible('.js-help-body')).to.be.false
    })

    it('Given the census theme is selected, when I click the "help and support" button, then the help should be visible', function() {

        // Given
        startCensusQuestionnaire('census_individual.json')

        // When
        browser.click('.js-help-btn')

        // Then
        expect(browser.isVisible('.js-help-body')).to.be.true
    })
})
