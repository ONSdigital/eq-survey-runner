const helpers = require('../../helpers');

const WhatIsYourAddress = require('../../pages/surveys/census/household/what-is-your-address.page');
const PermanentOrFamilyHome = require('../../pages/surveys/census/household/permanent-or-family-home.page');
const HouseholdComposition = require('../../pages/surveys/census/household/household-composition.page');
const HouseholdMemberBegin = require('../../pages/surveys/census/household/household-member-begin.page');
const DetailsCorrect = require('../../pages/surveys/census/household/details-correct.page');
const Over16 = require('../../pages/surveys/census/household/over-16.page');
const EmploymentType = require('../../pages/surveys/census/household/employment-type.page');
const MainJob = require('../../pages/surveys/census/household/main-job.page');
const JobSeeker = require('../../pages/surveys/census/household/jobseeker.page.js');


describe('Census Household', function () {

  it('Given I am answering question 28. Last week were you.., When I select none of the above, Then I am routed to 29. Were you actively looking for...?', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(helpers.navigationLink('John'))
          .click(HouseholdMemberBegin.submit())
          .click(DetailsCorrect.submit())
          .click(Over16.yes())
          .then(() => {
            return helpers.pressSubmit(20);
          })
          .then(() => {
          return browser
            .getUrl().should.eventually.contain(EmploymentType.pageName)
            .click(EmploymentType.noneOfTheAbove())
            .click(EmploymentType.submit())
            .getUrl().should.eventually.contain(JobSeeker.pageName);
      });
    });
  });

  it('Given I am answering question 28. Last week were you.., When I select multiple answers including none of the above, Then I am routed to 35. In your main job, are (were) you?', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(helpers.navigationLink('John'))
          .click(HouseholdMemberBegin.submit())
          .click(DetailsCorrect.submit())
          .click(Over16.yes())
          .then(() => {
            return helpers.pressSubmit(20);
          })
          .then(() => {
          return browser
            .getUrl().should.eventually.contain(EmploymentType.pageName)
            .click(EmploymentType.workingAsAnEmployee())
            .click(EmploymentType.onAGovernmentSponsoredTrainingScheme())
            .click(EmploymentType.noneOfTheAbove())
            .click(EmploymentType.submit())
            .getUrl().should.eventually.contain(MainJob.pageName);
      });
    });
  });

  it('Given I am answering question 28. Last week were you.., When I select multiple answers excluding none of the above, Then I am routed to 35. In your main job, are (were) you?', function () {
    return helpers.startCensusQuestionnaire('census_household.json')
      .then(() => {
        return browser
          .setValue(WhatIsYourAddress.addressLine1(), '44 hill side')
          .click(WhatIsYourAddress.submit())
          .click(PermanentOrFamilyHome.yes())
          .click(PermanentOrFamilyHome.submit())
          .setValue(HouseholdComposition.firstName(), 'John')
          .click(HouseholdComposition.submit())
          .click(helpers.navigationLink('John'))
          .click(HouseholdMemberBegin.submit())
          .click(DetailsCorrect.submit())
          .click(Over16.yes())
          .then(() => {
            return helpers.pressSubmit(20);
          })
          .then(() => {
          return browser
            .getUrl().should.eventually.contain(EmploymentType.pageName)

            .click(EmploymentType.workingAsAnEmployee())
            .click(EmploymentType.onAGovernmentSponsoredTrainingScheme())
            .click(EmploymentType.submit())
            .getUrl().should.eventually.contain(MainJob.pageName);
      });
    });
  });

});
