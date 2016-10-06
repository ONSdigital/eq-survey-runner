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

  submit = function() {
    browser.click('.qa-btn-submit-dev')
    return this
  }
}

export default new DevPage()
