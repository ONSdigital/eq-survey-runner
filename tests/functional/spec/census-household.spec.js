const helpers = require('../helpers');

const WhatIsYourAddress = require('../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../pages/surveys/census/household/household-composition.page');
const EveryoneAtAddressConfirmation = require('../pages/surveys/census/household/everyone-at-address-confirmation.page');
const OvernightVisitors = require('../pages/surveys/census/household/overnight-visitors.page');
const WhoLivesHereCompleted = require('../pages/surveys/census/household/who-lives-here-completed.page');
const TypeOfAccommodation = require('../pages/surveys/census/household/type-of-accommodation.page');
const TypeOfHouse = require('../pages/surveys/census/household/type-of-house.page');
const SelfContainedAccommodation = require('../pages/surveys/census/household/self-contained-accommodation.page');
const NumberOfBedrooms = require('../pages/surveys/census/household/number-of-bedrooms.page');
const CentralHeating = require('../pages/surveys/census/household/central-heating.page');
const OwnOrRent = require('../pages/surveys/census/household/own-or-rent.page');
const NumberOfVehicles = require('../pages/surveys/census/household/number-of-vehicles.page');
const HouseholdAndAccommodationCompleted = require('../pages/surveys/census/household/household-and-accommodation-completed.page');
const HouseholdMemberBegin = require('../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../pages/surveys/census/household/details-correct.page');
const Over16 = require('../pages/surveys/census/household/over-16.page');
const PrivateResponse = require('../pages/surveys/census/household/private-response.page');
const Sex = require('../pages/surveys/census/household/sex.page');
const DateOfBirth = require('../pages/surveys/census/household/date-of-birth.page');
const MaritalStatus = require('../pages/surveys/census/household/marital-status.page');
const AnotherAddress = require('../pages/surveys/census/household/another-address.page');
const InEducation = require('../pages/surveys/census/household/in-education.page');
const CountryOfBirth = require('../pages/surveys/census/household/country-of-birth.page');
const Carer = require('../pages/surveys/census/household/carer.page');
const NationalIdentity = require('../pages/surveys/census/household/national-identity.page');
const EthnicGroup = require('../pages/surveys/census/household/ethnic-group.page');
const WhiteEthnicGroup = require('../pages/surveys/census/household/white-ethnic-group.page');
const AsianEthnicGroup = require('../pages/surveys/census/household/asian-ethnic-group.page');
const BlackEthnicGroup = require('../pages/surveys/census/household/black-ethnic-group.page');
const UnderstandWelsh = require('../pages/surveys/census/household/understand-welsh.page');
const Language = require('../pages/surveys/census/household/language.page');
const Religion = require('../pages/surveys/census/household/religion.page');
const PastUsualAddress = require('../pages/surveys/census/household/past-usual-address.page');
const Passports = require('../pages/surveys/census/household/passports.page');
const Disability = require('../pages/surveys/census/household/disability.page');
const Qualifications = require('../pages/surveys/census/household/qualifications.page');
const EmploymentType = require('../pages/surveys/census/household/employment-type.page');
const Jobseeker = require('../pages/surveys/census/household/jobseeker.page');
const JobAvailability = require('../pages/surveys/census/household/job-availability.page');
const JobPending = require('../pages/surveys/census/household/job-pending.page');
const Occupation = require('../pages/surveys/census/household/occupation.page');
const EverWorked = require('../pages/surveys/census/household/ever-worked.page');
const MainJob = require('../pages/surveys/census/household/main-job.page');
const JobTitle = require('../pages/surveys/census/household/job-title.page');
const JobDescription = require('../pages/surveys/census/household/job-description.page');
const EmployersBusiness = require('../pages/surveys/census/household/employers-business.page');
const MainJobType = require('../pages/surveys/census/household/main-job-type.page');
const BusinessName = require('../pages/surveys/census/household/business-name.page');
const WorkPage = require('../pages/surveys/census/household/hours-worked.page.js');
const TravelPage = require('../pages/surveys/census/household/work-travel.page.js');
const HouseholdMemberCompleted = require('../pages/surveys/census/household/household-member-completed.page');
const VisitorBegin = require('../pages/surveys/census/household/visitor-begin.page');
const VisitorName = require('../pages/surveys/census/household/visitor-name.page');
const VisitorSex = require('../pages/surveys/census/household/visitor-sex.page');
const VisitorDateOfBirth = require('../pages/surveys/census/household/visitor-date-of-birth.page');
const VisitorUkResident = require('../pages/surveys/census/household/visitor-uk-resident.page');
const VisitorAddress = require('../pages/surveys/census/household/visitor-address.page');
const VisitorCompleted = require('../pages/surveys/census/household/visitor-completed.page');
const VisitorsCompleted = require('../pages/surveys/census/household/visitors-completed.page');
const Confirmation = require('../pages/confirmation.page');
const ThankYou = require('../pages/thank-you.page');


describe('Census Household', function () {

  it('Given a census household survey with welsh region, When i enter valid data, Then the survey should submit successfully', function () {
    return helpers.startCensusQuestionnaire('census_household.json', false, 'GB-WLS')
      .then(() => {
        return browser
        // who-lives-here
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(EveryoneAtAddressConfirmation.yes())
          .click(EveryoneAtAddressConfirmation.submit())
          .setValue(OvernightVisitors.answer(), 1)
          .click(OvernightVisitors.submit())
          .click(WhoLivesHereCompleted.submit());

      })
      .then(completeHouseholdAndAccommodation)
      .then(() => {

        // household-member
        return browser
          .click(HouseholdMemberBegin.submit())
          .click(DetailsCorrect.yesThisIsMyFullName())
          .click(DetailsCorrect.submit())
          .click(Over16.yes())
          .click(Over16.submit())
          .click(PrivateResponse.noIDoNotWantToRequestAPersonalForm())
          .click(PrivateResponse.submit())
          .click(Sex.male())
          .click(Sex.submit())
          .setValue(DateOfBirth.day(), 2)
          .selectByValue(DateOfBirth.month(), 4)
          .setValue(DateOfBirth.year(), 1980)
          .click(DateOfBirth.submit())
          .click(MaritalStatus.married())
          .click(MaritalStatus.submit())
          .click(AnotherAddress.no())
          .click(AnotherAddress.submit())
          .click(InEducation.no())
          .click(InEducation.submit())
          .click(CountryOfBirth.walesWales())
          .click(CountryOfBirth.submit())
          .click(Carer.no())
          .click(Carer.submit())
          .click(NationalIdentity.walesWelsh())
          .click(NationalIdentity.submit())
          .click(EthnicGroup.walesAsianAsianBritish())
          .click(EthnicGroup.submit())
          .click(AsianEthnicGroup.indian())
          .click(AsianEthnicGroup.submit())
          .click(UnderstandWelsh.noneOfTheAbove())
          .click(UnderstandWelsh.submit())
          .click(Language.welshEnglishOrWelsh())
          .click(Language.submit())
          .click(Religion.noReligion())
          .click(Religion.submit())
          .click(PastUsualAddress.thisAddress())
          .click(Passports.submit())
          .click(Passports.unitedKingdom())
          .click(Passports.submit())
          .click(Disability.no())
          .click(Disability.submit())
          .click(Qualifications.welshUndergraduateDegree())
          .click(Qualifications.submit())
          .click(EmploymentType.workingAsAnEmployee())
          .click(EmploymentType.onAGovernmentSponsoredTrainingScheme())
          .click(EmploymentType.submit())
          .click(MainJob.anEmployee())
          .click(MainJob.submit())
          .click(WorkPage.answer3148())
          .click(WorkPage.submit())
          .click(TravelPage.train())
          .click(TravelPage.submit())
          .setValue(JobTitle.answer(), 'Dev')
          .click(JobTitle.submit())
          .setValue(JobDescription.answer(), 'writing lots of code')
          .click(JobDescription.submit())
          .click(MainJobType.employedByAnOrganisationOrBusiness())
          .click(MainJobType.submit())
          .setValue(BusinessName.answer(), 'ONS')
          .click(BusinessName.submit())
          .setValue(EmployersBusiness.answer(), 'something statistical')
          .click(EmployersBusiness.submit())
          .click(HouseholdMemberCompleted.submit());

      })
      .then(completeVisitorSection)
      .then(() => {
        return browser
          .click(VisitorsCompleted.submit())
          .click(Confirmation.submit())
          .getUrl().should.eventually.contain(ThankYou.pageName);

      });

  });

    it('Given a census household survey, when a user submits the household composition page with errors, adding a new person should not duplicate those errors', function() {
      return helpers.startCensusQuestionnaire('census_household.json')
        .then(() => {
          return browser
            .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
            .click(WhatIsYourAddress.submit())
            .click(PermanentOrFamilyHome.yes())
            .click(PermanentOrFamilyHome.submit())
            .click(HouseholdComposition.submit())
            .click(HouseholdComposition.addPerson())
            .$$('.js-household-person .js-has-errors').should.eventually.have.lengthOf(1);
        });
    });
});

function completeHouseholdAndAccommodation() {
  return browser
    .click(TypeOfAccommodation.wholeHouseOrBungalow())
    .click(TypeOfAccommodation.submit())
    .click(TypeOfHouse.semiDetached())
    .click(TypeOfHouse.submit())
    .click(SelfContainedAccommodation.yesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse())
    .click(SelfContainedAccommodation.submit())
    .setValue(NumberOfBedrooms.answer(), 3)
    .click(NumberOfBedrooms.submit())
    .click(CentralHeating.gas())
    .click(CentralHeating.submit())
    .click(OwnOrRent.ownsOutright())
    .click(OwnOrRent.submit())
    .setValue(NumberOfVehicles.answer(), 2)
    .click(NumberOfVehicles.submit())
    .click(HouseholdAndAccommodationCompleted.submit());
}

function completeVisitorSection() {
  return browser
    .click(VisitorBegin.submit())
    .setValue(VisitorName.visitorFirstName(), 'Jane')
    .setValue(VisitorName.visitorLastName(), 'Doe')
    .click(VisitorName.submit())
    .click(VisitorSex.female())
    .click(VisitorSex.submit())
    .setValue(VisitorDateOfBirth.day(), 10)
    .selectByValue(VisitorDateOfBirth.month(), 7)
    .setValue(VisitorDateOfBirth.year(), 1990)
    .click(VisitorDateOfBirth.submit())
    .click(VisitorUkResident.yesUsuallyLivesInTheUnitedKingdom())
    .click(VisitorUkResident.submit())
    .setValue(VisitorAddress.building(), 50)
    .setValue(VisitorAddress.street(), 'My Road')
    .setValue(VisitorAddress.city(), 'Newport')
    .setValue(VisitorAddress.postcode(), 'AB123CD')
    .click(VisitorAddress.submit())
    .click(VisitorCompleted.submit());
}
