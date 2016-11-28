class DevPage {

  open() {
    browser.url('/dev')
    return this
  }

  setUserId(userId) {
    browser.setValue('.qa-user-id', userId)
    return this
  }

  setCollectionId(collectionId) {
    browser.setValue('.qa-collection-sid', collectionId)
    return this
  }

  setSchema(schema) {
    browser.selectByValue('.qa-select-schema', schema)
    return this
  }

  setPeriodId(period_id) {
    browser.setValue('.qa-period-id', period_id)
    return this
  }

  setPeriodString(period_str) {
    browser.setValue('.qa-period-str', period_str)
    return this
  }

  setRegionCode(region) {
    browser.selectByValue('.qa-region-code', region)
    return this
  }

  checkSexualIdentity() {
    browser.click('.qa-sexual-identity')
    return this
  }

  submit() {
    browser.click('.qa-btn-submit-dev')
    return this
  }
}

export default new DevPage()
