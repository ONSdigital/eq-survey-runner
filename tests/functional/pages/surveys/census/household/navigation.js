class Navigation {

  navigateToHouseholdAndAccommodation() {
    return browser.element('//a[text()="Household and Accommodation"]').click()
  }

}

export default new Navigation()
