// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LandlordPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('landlord')
  }

  clickLandlordAnswerHousingAssociationHousingCoOperativeCharitableTrustRegisteredSocialLandlord() {
    browser.element('[id="landlord-answer-0"]').click()
    return this
  }

  clickLandlordAnswerCouncilLocalAuthority() {
    browser.element('[id="landlord-answer-1"]').click()
    return this
  }

  clickLandlordAnswerPrivateLandlordOrLettingAgency() {
    browser.element('[id="landlord-answer-2"]').click()
    return this
  }

  clickLandlordAnswerEmployerOfAHouseholdMember() {
    browser.element('[id="landlord-answer-3"]').click()
    return this
  }

  clickLandlordAnswerRelativeOrFriendOfAHouseholdMember() {
    browser.element('[id="landlord-answer-4"]').click()
    return this
  }

  clickLandlordAnswerOther() {
    browser.element('[id="landlord-answer-5"]').click()
    return this
  }

}

export default new LandlordPage()
