const helpers = require('../helpers');

const EstablishmentTypePage = require('../pages/surveys/census/communal/establishment-type.page.js');
const BedSpacesPage = require('../pages/surveys/census/communal/bed-spaces.page.js');
const UsualResidentsPage = require('../pages/surveys/census/communal/usual-residents.page.js');
const UsualResidentsNumberPage = require('../pages/surveys/census/communal/usual-residents-number.page.js');
const DescribeResidentsPage = require('../pages/surveys/census/communal/describe-residents.page.js');
const CompletionPreferenceIndividualPage = require('../pages/surveys/census/communal/completion-preference-individual.page.js');
const WhyPaperIndividualPage = require('../pages/surveys/census/communal/why-paper-individual.page.js');
const CompletionPreferenceEstablishmentPage = require('../pages/surveys/census/communal/completion-preference-establishment.page.js');
const WhyPaperEstablishmentPage = require('../pages/surveys/census/communal/why-paper-establishment.page.js');
const FurtherContactPage = require('../pages/surveys/census/communal/further-contact.page.js');
const ContactDetailsPage = require('../pages/surveys/census/communal/contact-details.page.js');
const ConfirmationPage = require('../pages/surveys/census/communal/confirmation.page.js');
const ThankYou = require('../pages/thank-you.page');

describe('Census Communal', function() {

  it('Given Respondent Home has identified the respondent should have the Communal Establishment Questionnaire, When I complete the EQ, Then i should be able to successfully submit', function() {
    return helpers.openQuestionnaire('census_communal.json').then(() => {
        return browser
          .click(EstablishmentTypePage.hotel())
          .click(EstablishmentTypePage.submit())
          .setValue(BedSpacesPage.answer(),20)
          .click(BedSpacesPage.submit())
          .click(UsualResidentsPage.yes())
          .click(UsualResidentsPage.submit())
          .setValue(UsualResidentsNumberPage.answer(),10)
          .click(UsualResidentsNumberPage.submit())
          .click(DescribeResidentsPage.payingGuests())
          .click(DescribeResidentsPage.submit())
          .click(CompletionPreferenceIndividualPage.paper())
          .click(CompletionPreferenceIndividualPage.submit())
          .click(WhyPaperIndividualPage.moreConvenient())
          .click(WhyPaperIndividualPage.submit())
          .click(CompletionPreferenceEstablishmentPage.paper())
          .click(CompletionPreferenceEstablishmentPage.submit())
          .click(WhyPaperEstablishmentPage.moreConvenient())
          .click(WhyPaperEstablishmentPage.submit())
          .click(FurtherContactPage.yes())
          .click(FurtherContactPage.submit())
          .setValue(ContactDetailsPage.name(),"John Smith")
          .setValue(ContactDetailsPage.email(),"john@mmith.co.uk")
          .setValue(ContactDetailsPage.phone(),"09876543210")
          .click(UsualResidentsNumberPage.submit())
          .click(ConfirmationPage.submit())
          .getUrl().should.eventually.contain(ThankYou.pageName);
    });
  });

  it('Given Respondent Home has identified the respondent should have the Communal Establishment Questionnaire, When I complete the EQ with 0 bed spaces, Then i should be routed to further contact', function() {
    return helpers.openQuestionnaire('census_communal.json').then(() => {
        return browser
          .click(EstablishmentTypePage.hotel())
          .click(EstablishmentTypePage.submit())
          .setValue(BedSpacesPage.answer(),0)
          .click(BedSpacesPage.submit())
          .click(FurtherContactPage.yes())
          .click(FurtherContactPage.submit())
          .setValue(ContactDetailsPage.name(),"John Smith")
          .setValue(ContactDetailsPage.email(),"john@mmith.co.uk")
          .setValue(ContactDetailsPage.phone(),"09876543210")
          .click(UsualResidentsNumberPage.submit())
          .click(ConfirmationPage.submit())
          .getUrl().should.eventually.contain(ThankYou.pageName);
    });
  });


  it('Given Respondent Home has identified the respondent should have the Communal Establishment Questionnaire, When I complete the EQ with 2 bed spaces, Then i should be routed to UsualResidentsPage', function() {
    return helpers.openQuestionnaire('census_communal.json').then(() => {
        return browser
          .click(EstablishmentTypePage.hotel())
          .click(EstablishmentTypePage.submit())
          .setValue(BedSpacesPage.answer(),2)
          .click(BedSpacesPage.submit())
          .click(UsualResidentsPage.no())
          .click(UsualResidentsPage.submit())
          .getUrl().should.eventually.contain(CompletionPreferenceEstablishmentPage.pageName);
    });
  });
});
