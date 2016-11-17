import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LandlordPage extends MultipleChoiceWithOtherPage {

  clickHousingAssociationHousingCoOperativeCharitableTrustRegisteredSocialLandlord() {
    browser.element('[id="landlord-answer-1"]').click()
    return this
  }

  clickCouncilLocalAuthority() {
    browser.element('[id="landlord-answer-2"]').click()
    return this
  }

  clickPrivateLandlordOrLettingAgency() {
    browser.element('[id="landlord-answer-3"]').click()
    return this
  }

  clickEmployerOfAHouseholdMember() {
    browser.element('[id="landlord-answer-4"]').click()
    return this
  }

  clickRelativeOrFriendOfAHouseholdMember() {
    browser.element('[id="landlord-answer-5"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="landlord-answer-6"]').click()
    return this
  }

  setLandlordAnswer(value) {
    browser.setValue('[name="landlord-answer"]', value)
    return this
  }

  getLandlordAnswer(value) {
    return browser.element('[name="landlord-answer"]').getValue()
  }

}

export default new LandlordPage()
