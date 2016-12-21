class Navigation {

  navigateToHouseholdAndAccommodation() {
    browser.element('[data-qa="navigate-to-household-and-accommodation"]').click()
    return this
  }

}

export default new Navigation()
