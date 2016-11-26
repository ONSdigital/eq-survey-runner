import QuestionPage from '../question.page'

class ConditionalRoutingPage extends QuestionPage {

  clickYes(){
    browser.element('input[value="yes"]').click()
    return this
  }

  clickNo(){
    browser.element('input[value="no"]').click()
    return this
  }

  isBlock(blockId) {
    return this.getCurrentBlockId() === blockId
  }

  isGroup(groupId) {
    return this.getCurrentGroupId() === groupId
  }

  setNumberOfRepeats(numberOfRepeats) {
    browser.setValue('input[name="no-of-repeats-answer"]', numberOfRepeats)
    return this
  }

  clickAgeAndShoeSize() {
    browser.element('input[id="conditional-answer-1"]').click()
    return this
  }

  clickShoeSizeOnly() {
    browser.element('input[id="conditional-answer-2"]').click()
    return this
  }

  setAge() {
    browser.setValue('input[name="5667e5eb-f9d3-4482-9257-edf752000708"]', this.getRandomInt(16, 99))
    return this
  }

  setShoeSize() {
    browser.setValue('input[name="eccada31-f214-4bf2-9239-11487914c9d3"]', this.getRandomInt(4, 13))
    return this
  }

  getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min
  }

  getCurrentBlockId() {
    var url = browser.getUrl()
    return url.substr(url.lastIndexOf('/') + 1)
  }

  getCurrentGroupId() {
    return this.getCurrentLocation().groupId
  }

  getCurrentLocation() {
    // Matches: /(groupId)/(blockId)
    var regexp = /questionnaire.+\/(\d+)\/(.+)$/g
    var matches = regexp.exec(browser.getUrl())

    if (matches != null) {
      return {
        'groupId': matches[1],
        'blockId': matches[2]
      }
    } else {
      console.log('ERROR: URL did not match RegExp')
      console.log('> ' + browser.getUrl())
    }
  }

  completeBlocks(numberOfRepeats) {
    var i
    for (i = 0; i < numberOfRepeats; i++) {
      this.clickAgeAndShoeSize()
          .submit()
          .setAge()
          .submit()
          .setShoeSize()
          .submit()
    }
    return this
  }

}

export default new ConditionalRoutingPage()
