const helpers = require('../helpers/census');

const ThankYou = require('../../base_pages/thank-you.page.js');

const WhoLivesHereBlock = require('../../generated_pages/census_household/who-lives-here-block.page');
const PermanentOrFamilyHome = require('../../generated_pages/census_household/permanent-or-family-home.page');
const HouseholdComposition = require('../../generated_pages/census_household/household-composition.page');
const EveryoneAtAddressConfirmation = require('../../generated_pages/census_household/everyone-at-address-confirmation.page');
const OvernightVisitors = require('../../generated_pages/census_household/overnight-visitors.page');
const WhoLivesHereCompleted = require('../../generated_pages/census_household/who-lives-here-completed.page');
const HouseholdAndAccommodationBlock = require('../../generated_pages/census_household/household-and-accommodation-block.page');
const TypeOfAccommodation = require('../../generated_pages/census_household/type-of-accommodation.page');
const TypeOfHouse = require('../../generated_pages/census_household/type-of-house.page');
const SelfContainedAccommodation = require('../../generated_pages/census_household/self-contained-accommodation.page');
const NumberOfBedrooms = require('../../generated_pages/census_household/number-of-bedrooms.page');
const CentralHeating = require('../../generated_pages/census_household/central-heating.page');
const OwnOrRent = require('../../generated_pages/census_household/own-or-rent.page');
const NumberOfVehicles = require('../../generated_pages/census_household/number-of-vehicles.page');
const HouseholdAndAccommodationCompleted = require('../../generated_pages/census_household/household-and-accommodation-completed.page');
const HouseholdMemberBegin = require('../../generated_pages/census_household/household-member-begin-section.page');
const HouseholdRelationships = require('../../generated_pages/census_household/household-relationships.page');
const Sex = require('../../generated_pages/census_household/sex.page');
const DateOfBirth = require('../../generated_pages/census_household/date-of-birth.page');
const ConfirmDob = require('../../generated_pages/census_household/confirm-dob.page');
const ConfirmDobProxy = require('../../generated_pages/census_household/confirm-dob-proxy.page');
const MarriageType = require('../../generated_pages/census_household/marriage-type.page');
const CurrentMarriageStatus = require('../../generated_pages/census_household/current-marriage-status.page');
const AnotherAddress = require('../../generated_pages/census_household/another-address.page');
const InEducationOver16 = require('../../generated_pages/census_household/in-education-over16.page');
const CountryOfBirth = require('../../generated_pages/census_household/country-of-birth.page');
const Carer = require('../../generated_pages/census_household/carer.page');
const CarerProxy = require('../../generated_pages/census_household/carer-proxy.page');
const NationalIdentity = require('../../generated_pages/census_household/national-identity.page');
const EthnicGroup = require('../../generated_pages/census_household/ethnic-group.page');
const AsianEthnicGroup = require('../../generated_pages/census_household/asian-ethnic-group.page');
const WhiteEthnicGroup = require('../../generated_pages/census_household/white-ethnic-group.page');
const Language = require('../../generated_pages/census_household/language.page');
const Religion = require('../../generated_pages/census_household/religion.page');
const PastUsualAddress = require('../../generated_pages/census_household/past-usual-address.page');
const Passports = require('../../generated_pages/census_household/passports.page');
const Disability = require('../../generated_pages/census_household/disability.page');
const Qualifications = require('../../generated_pages/census_household/qualifications.page');
const EmploymentStatus = require('../../generated_pages/census_household/employment-status.page');
const JobTitle = require('../../generated_pages/census_household/job-title.page');
const JobDescription = require('../../generated_pages/census_household/job-description.page');
const EmployersBusiness = require('../../generated_pages/census_household/employers-business.page');
const MainJobType = require('../../generated_pages/census_household/main-job-type.page');
const BusinessName = require('../../generated_pages/census_household/business-name.page');
const BusinessNameProxy = require('../../generated_pages/census_household/business-name-proxy.page');
const HoursWorkedPage = require('../../generated_pages/census_household/hours-worked.page.js');
const HouseholdMemberCompleted = require('../../generated_pages/census_household/household-member-completed.page');
const VisitorBegin = require('../../generated_pages/census_household/visitor-begin-section.page');
const VisitorName = require('../../generated_pages/census_household/visitor-name.page');
const VisitorSex = require('../../generated_pages/census_household/visitor-sex.page');
const VisitorDateOfBirth = require('../../generated_pages/census_household/visitor-date-of-birth.page');
const VisitorUkResident = require('../../generated_pages/census_household/visitor-uk-resident.page');
const VisitorAddress = require('../../generated_pages/census_household/visitor-address.page');
const VisitorCompleted = require('../../generated_pages/census_household/visitor-completed.page');
const VisitorsCompleted = require('../../generated_pages/census_household/visitors-completed.page');
const Proxy = require('../../generated_pages/census_household/proxy.page');
const Health = require('../../generated_pages/census_household/health.page');
const SexualIdentity = require('../../generated_pages/census_household/sexual-identity.page');
const SexualIdentityProxy = require('../../generated_pages/census_household/sexual-identity-proxy.page');
const BirthGender = require('../../generated_pages/census_household/birth-gender.page');
const ArmedForces = require('../../generated_pages/census_household/armed-forces.page');
const Apprenticeship = require('../../generated_pages/census_household/apprenticeship.page');
const Degree = require('../../generated_pages/census_household/degree.page');
const MainEmploymentBlock = require('../../generated_pages/census_household/main-employment-block.page');
const ProfessionalQuals = require('../../generated_pages/census_household/professional-quals.page');
const Supervise = require('../../generated_pages/census_household/supervise.page');
const WorkTravel = require('../../generated_pages/census_household/work-travel.page');
const EmployerAddress = require('../../generated_pages/census_household/employer-address.page');
const EmployerTypeOfAddress = require('../../generated_pages/census_household/employer-type-of-address.page');
const Confirmation = require('../../generated_pages/census_household/confirmation.page');
const UnderstandWelsh = require('../../generated_pages/census_household/understand-welsh.page');


function completeHouseholdAndAccommodation() {
  return cy
    .get(HouseholdAndAccommodationBlock.submit()).click()
    .get(TypeOfAccommodation.wholeHouseOrBungalow()).click()
    .get(TypeOfAccommodation.submit()).click()
    .get(TypeOfHouse.semiDetached()).click()
    .get(TypeOfHouse.submit()).click()
    .get(SelfContainedAccommodation.yes()).click()
    .get(SelfContainedAccommodation.submit()).click()
    .get(NumberOfBedrooms.answer()).type(3)
    .get(NumberOfBedrooms.submit()).click()
    .get(CentralHeating.mainsGas()).click()
    .get(CentralHeating.submit()).click()
    .get(OwnOrRent.ownsOutright()).click()
    .get(OwnOrRent.submit()).click()
    .get(NumberOfVehicles.answer2()).click()
    .get(NumberOfVehicles.submit()).click()
    .get(HouseholdAndAccommodationCompleted.submit()).click();
}

function completeVisitorSection() {
  return cy
    .get(VisitorBegin.submit()).click()
    .get(VisitorName.visitorFirstName()).type('Jane')
    .get(VisitorName.visitorLastName()).type('Doe')
    .get(VisitorName.submit()).click()
    .get(VisitorSex.female()).click()
    .get(VisitorSex.submit()).click()
    .get(VisitorDateOfBirth.day()).type(10)
    .get(VisitorDateOfBirth.month()).select("7")
    .get(VisitorDateOfBirth.year()).type(1990)
    .get(VisitorDateOfBirth.submit()).click()
    .get(VisitorUkResident.yesUsuallyLivesInTheUnitedKingdom()).click()
    .get(VisitorUkResident.submit()).click()
    .get(VisitorAddress.building()).type(50)
    .get(VisitorAddress.street()).type('My Road')
    .get(VisitorAddress.city()).type('Newport')
    .get(VisitorAddress.postcode()).type('AB123CD')
    .get(VisitorAddress.submit()).click()
    .get(VisitorCompleted.submit()).click();
}

context('Census Household', () => {

    it('Given a census household survey with welsh region, When i enter valid data, Then the survey should submit successfully', function () {

        return helpers.openCensusQuestionnaire('census_household.json', false, 'GB-WLS')
            .then(() => {
                return cy
                  .get(WhoLivesHereBlock.submit()).click()
                  .get(PermanentOrFamilyHome.yes()).click()
                  .get(PermanentOrFamilyHome.submit()).click()
                  .get(HouseholdComposition.addPerson()).click()
                  .get(HouseholdComposition.firstName()).type('John')
                  .get(HouseholdComposition.lastName()).type('Smith')
                  .get(HouseholdComposition.firstName('_1')).type('Jane')
                  .get(HouseholdComposition.lastName('_1')).type('Smith')
                  .get(HouseholdComposition.submit()).click()
                  .get(EveryoneAtAddressConfirmation.yes()).click()
                  .get(EveryoneAtAddressConfirmation.submit()).click()
                  .get(OvernightVisitors.answer()).type(1)
                  .get(OvernightVisitors.submit()).click()
                  .get(HouseholdRelationships.answer('0')).select('Husband or wife')
                  .get(HouseholdRelationships.submit()).click()
                  .get(WhoLivesHereCompleted.submit()).click();
            })
            .then(completeHouseholdAndAccommodation)
            .then(() => {
                return cy
                  .get(HouseholdMemberBegin.submit()).click()
                  .get(Proxy.questionText()).should((questionText) => {
                    expect(questionText).to.contain('John Smith');
                  })
                  .get(Proxy.yesIAm()).click()
                  .get(Proxy.submit()).click()
                  .get(Sex.male()).click()
                  .get(Sex.submit()).click()
                  .get(DateOfBirth.day()).type(2)
                  .get(DateOfBirth.month()).select("4")
                  .get(DateOfBirth.year()).type(1980)
                  .get(DateOfBirth.submit()).click()
                  .get(ConfirmDob.yes()).click()
                  .get(ConfirmDob.submit()).click()
                  .get(MarriageType.married()).click()
                  .get(MarriageType.submit()).click()
                  .get(CurrentMarriageStatus.someoneOfTheOppositeSex()).click()
                  .get(CurrentMarriageStatus.submit()).click()
                  .get(AnotherAddress.no()).click()
                  .get(AnotherAddress.submit()).click()
                  .get(InEducationOver16.no()).click()
                  .get(InEducationOver16.submit()).click()
                  .get(CountryOfBirth.walesWales()).click()
                  .get(CountryOfBirth.submit()).click()
                  .get(Health.good()).click()
                  .get(Health.submit()).click()
                  .get(Disability.no()).click()
                  .get(Disability.submit()).click()
                  .get(Carer.no()).click()
                  .get(Carer.submit()).click()
                  .get(NationalIdentity.walesWelsh()).click()
                  .get(NationalIdentity.submit()).click()
                  .get(EthnicGroup.walesAsianOrAsianBritish()).click()
                  .get(EthnicGroup.submit()).click()
                  .get(AsianEthnicGroup.indian()).click()
                  .get(AsianEthnicGroup.submit()).click()
                  .get(SexualIdentity.straightOrHeterosexual()).click()
                  .get(SexualIdentity.submit()).click()
                  .get(BirthGender.yes()).click()
                  .get(BirthGender.submit()).click()
                  .get(UnderstandWelsh.understandSpokenWelsh()).click()
                  .get(UnderstandWelsh.submit()).click()
                  .get(Language.welshEnglishOrWelsh()).click()
                  .get(Language.submit()).click()
                  .get(Religion.noReligion()).click()
                  .get(Religion.submit()).click()
                  .get(PastUsualAddress.householdaddress()).click()
                  .get(PastUsualAddress.submit()).click()
                  .get(Passports.unitedKingdom()).click()
                  .get(Passports.submit()).click()
                  .get(ArmedForces.no()).click()
                  .get(ArmedForces.submit()).click()
                  .get(Qualifications.submit()).click()
                  .get(Apprenticeship.no()).click()
                  .get(Apprenticeship.submit()).click()
                  .get(Degree.yes()).click()
                  .get(Degree.submit()).click()
                  .get(EmploymentStatus.workingAsAnEmployee()).click()
                  .get(EmploymentStatus.submit()).click()
                  .get(MainEmploymentBlock.submit()).click()
                  .get(MainJobType.employee()).click()
                  .get(MainJobType.submit()).click()
                  .get(BusinessName.answer()).type('ONS')
                  .get(BusinessName.submit()).click()
                  .get(JobTitle.answer()).type('Dev')
                  .get(JobTitle.submit()).click()
                  .get(JobDescription.answer()).type('writing lots of code')
                  .get(JobDescription.submit()).click()
                  .get(EmployersBusiness.questionText()).should((questionText) => {
                    expect(questionText).to.contain('ONS');
                  })
                  .get(EmployersBusiness.answer()).type('something statistical')
                  .get(EmployersBusiness.submit()).click()
                  .get(ProfessionalQuals.no()).click()
                  .get(ProfessionalQuals.submit()).click()
                  .get(Supervise.no()).click()
                  .get(Supervise.submit()).click()
                  .get(HoursWorkedPage.answer31To48Hours()).click()
                  .get(HoursWorkedPage.submit()).click()
                  .get(WorkTravel.train()).click()
                  .get(WorkTravel.submit()).click()
                  .get(EmployerTypeOfAddress.atAWorkplace()).click()
                  .get(EmployerTypeOfAddress.submit()).click()
                  .get(EmployerAddress.building()).type('Government Buildings')
                  .get(EmployerAddress.street()).type('Cardiff Road')
                  .get(EmployerAddress.city()).type('Newport')
                  .get(EmployerAddress.postcode()).type('NP10 8XG')
                  .get(EmployerAddress.submit()).click()
                  .get(HouseholdMemberCompleted.interstitialHeader()).should((header) => {
                    expect(header).to.contain('John Smith');
                  })
                  .get(HouseholdMemberCompleted.submit()).click();
            })
            .then(() => {
                return cy
                  .get(HouseholdMemberBegin.submit()).click()
                  .get(Proxy.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Proxy.proxy()).click()
                  .get(Proxy.submit()).click()
                  .get(Sex.questionText()).contains('Jane Smith')
                  .get(Sex.female()).click()
                  .get(Sex.submit()).click()
                  .get(DateOfBirth.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(DateOfBirth.day()).type(12)
                  .get(DateOfBirth.month()).select("9")
                  .get(DateOfBirth.year()).type(1979)
                  .get(DateOfBirth.submit()).click()
                  .get(ConfirmDobProxy.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(ConfirmDobProxy.yes()).click()
                  .get(ConfirmDobProxy.submit()).click()
                  .get(MarriageType.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(MarriageType.married()).click()
                  .get(MarriageType.submit()).click()
                  .get(CurrentMarriageStatus.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(CurrentMarriageStatus.someoneOfTheOppositeSex()).click()
                  .get(CurrentMarriageStatus.submit()).click()
                  .get(AnotherAddress.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(AnotherAddress.no()).click()
                  .get(AnotherAddress.submit()).click()
                  .get(InEducationOver16.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(InEducationOver16.no()).click()
                  .get(InEducationOver16.submit()).click()
                  .get(CountryOfBirth.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(CountryOfBirth.walesWales()).click()
                  .get(CountryOfBirth.submit()).click()
                  .get(Health.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Health.good()).click()
                  .get(Health.submit()).click()
                  .get(Disability.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Disability.no()).click()
                  .get(Disability.submit()).click()
                  .get(CarerProxy.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(CarerProxy.no()).click()
                  .get(CarerProxy.submit()).click()
                  .get(NationalIdentity.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(NationalIdentity.walesWelsh()).click()
                  .get(NationalIdentity.submit()).click()
                  .get(EthnicGroup.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(EthnicGroup.walesWhite()).click()
                  .get(EthnicGroup.submit()).click()
                  .get(WhiteEthnicGroup.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(WhiteEthnicGroup.walesWelshEnglishScottishNorthernIrishOrBritish()).click()
                  .get(WhiteEthnicGroup.submit()).click()
                  .get(SexualIdentityProxy.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(SexualIdentityProxy.straightOrHeterosexual()).click()
                  .get(SexualIdentityProxy.submit()).click()
                  .get(BirthGender.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(BirthGender.yes()).click()
                  .get(BirthGender.submit()).click()
                  .get(UnderstandWelsh.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(UnderstandWelsh.understandSpokenWelsh()).click()
                  .get(UnderstandWelsh.submit()).click()
                  .get(Language.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Language.welshEnglishOrWelsh()).click()
                  .get(Language.submit()).click()
                  .get(Religion.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Religion.noReligion()).click()
                  .get(Religion.submit()).click()
                  .get(PastUsualAddress.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(PastUsualAddress.householdaddress()).click()
                  .get(PastUsualAddress.submit()).click()
                  .get(Passports.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Passports.unitedKingdom()).click()
                  .get(Passports.submit()).click()
                  .get(ArmedForces.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(ArmedForces.no()).click()
                  .get(ArmedForces.submit()).click()
                  .get(Qualifications.submit()).click()
                  .get(Apprenticeship.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Apprenticeship.no()).click()
                  .get(Apprenticeship.submit()).click()
                  .get(Degree.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Degree.yes()).click()
                  .get(Degree.submit()).click()
                  .get(EmploymentStatus.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(EmploymentStatus.workingAsAnEmployee()).click()
                  .get(EmploymentStatus.submit()).click()
                  .get(MainEmploymentBlock.submit()).click()
                  .get(MainJobType.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(MainJobType.employee()).click()
                  .get(MainJobType.submit()).click()
                  .get(BusinessNameProxy.answer()).type('ONS')
                  .get(BusinessNameProxy.submit()).click()
                  .get(JobTitle.answer()).type('Dev')
                  .get(JobTitle.submit()).click()
                  .get(JobDescription.answer()).type('writing lots of code')
                  .get(JobDescription.submit()).click()
                  .get(EmployersBusiness.questionText()).contains('ONS')
                  .get(EmployersBusiness.answer()).type('something statistical')
                  .get(EmployersBusiness.submit()).click()
                  .get(ProfessionalQuals.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(ProfessionalQuals.no()).click()
                  .get(ProfessionalQuals.submit()).click()
                  .get(Supervise.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(Supervise.no()).click()
                  .get(Supervise.submit()).click()
                  .get(HoursWorkedPage.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(HoursWorkedPage.answer31To48Hours()).click()
                  .get(HoursWorkedPage.submit()).click()
                  .get(WorkTravel.questionText()).should((questionText) => {
                    expect(questionText).to.contain('Jane Smith');
                  })
                  .get(WorkTravel.drivingACarOrVan()).click()
                  .get(WorkTravel.submit()).click()
                  .get(EmployerTypeOfAddress.atAWorkplace()).click()
                  .get(EmployerTypeOfAddress.submit()).click()
                  .get(EmployerAddress.building()).type('Government Buildings')
                  .get(EmployerAddress.street()).type('Cardiff Road')
                  .get(EmployerAddress.city()).type('Newport')
                  .get(EmployerAddress.postcode()).type('NP10 8XG')
                  .get(EmployerAddress.submit()).click()
                  .get(HouseholdMemberCompleted.interstitialHeader()).should((header) => {
                    expect(header).to.contain('Jane Smith');
                  })
                  .get(HouseholdMemberCompleted.submit()).click();
            })
            .then(completeVisitorSection)
            .then(() => {
                return cy
                  .get(VisitorsCompleted.submit()).click()
                  .get(Confirmation.submit()).click()
                  .location().should((loc) => {
                    expect(loc.pathname).to.include(ThankYou.pageName);
                  });
            });
    });
});
