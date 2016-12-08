import chai from 'chai'
import {openQuestionnaire} from '../helpers'

import EstablishmentType from '../pages/surveys/census/communal/establishment-type.page.js'
import BedSpaces from '../pages/surveys/census/communal/bed-spaces.page.js'
import UsualResidents from '../pages/surveys/census/communal/usual-residents.page.js'
import UsualResidentsNumber from '../pages/surveys/census/communal/usual-residents-number.page.js'
import DescribeResidents from '../pages/surveys/census/communal/describe-residents.page.js'
import CompletionPreferenceIndividual from '../pages/surveys/census/communal/completion-preference-individual.page.js'
import WhyPaperIndividual from '../pages/surveys/census/communal/why-paper-individual.page.js'
import CompletionPreferenceEstablishment from '../pages/surveys/census/communal/completion-preference-establishment.page.js'
import WhyPaperEstablishment from '../pages/surveys/census/communal/why-paper-establishment.page.js'
import FurtherContact from '../pages/surveys/census/communal/further-contact.page.js'
import ContactDetails from '../pages/surveys/census/communal/contact-details.page.js'
import Confirmation from '../pages/confirmation.page.js'
import ThankYou from '../pages/thank-you.page'

const expect = chai.expect

describe('Example Test', function() {

  it('Given Respondent Home has identified the respondent should have the Communal Establishment Questionnaire, When I complete the EQ, Then i should be able to successfully submit', function() {
      openQuestionnaire('census_communal.json')

      EstablishmentType.clickEstablishmentTypeAnswerHotel().submit()
      BedSpaces.setBedSpacesAnswer(20).submit()
      UsualResidents.clickUsualResidentsAnswerYes().submit()
      UsualResidentsNumber.setUsualResidentsNumberAnswer(10).submit()
      DescribeResidents.clickDescribeResidentsAnswerPayingGuests().submit()
      CompletionPreferenceIndividual.clickCompletionPreferenceIndividualAnswerPaper().submit()
      WhyPaperIndividual.clickWhyPaperIndividualAnswerUnsureHowToUseAComputer().submit()
      CompletionPreferenceEstablishment.clickCompletionPreferenceEstablishmentAnswerPaper().submit()
      WhyPaperEstablishment.clickWhyPaperEstablishmentAnswerMoreConvenient().submit()
      FurtherContact.clickFurtherContactAnswerYes().submit()
      ContactDetails.setContactDetailsAnswerName("John Smith").setContactDetailsAnswerEmail("jon@smith.com").setContactDetailsAnswerPhone("098765432347").submit()

      Confirmation.submit()

      // Thank You
      expect(ThankYou.isOpen()).to.be.true
  })

  it('Given Respondent Home has identified the respondent should have the Communal Establishment Questionnaire, When I complete the EQ with 0 bed spaces, Then i should be routed to further contact', function() {
      openQuestionnaire('census_communal.json')

      EstablishmentType.clickEstablishmentTypeAnswerHotel().submit()
      BedSpaces.setBedSpacesAnswer(0).submit()
      FurtherContact.clickFurtherContactAnswerYes().submit()
      ContactDetails.setContactDetailsAnswerName("John Smith").setContactDetailsAnswerEmail("jon@smith.com").setContactDetailsAnswerPhone("098765432347").submit()

      Confirmation.submit()

      // Thank You
      expect(ThankYou.isOpen()).to.be.true
  })

})

