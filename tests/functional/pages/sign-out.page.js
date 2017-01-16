class SignOut {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('signed-out') > -1
  }
}
export default new SignOut()
