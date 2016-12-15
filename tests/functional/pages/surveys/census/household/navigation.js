class Navigation {

  navigateToHouseholdAndAccommodation() {
    browser.element('//a[text()="Household and Accommodation"]').click()
    return this
  }

}

export default new Navigation()
