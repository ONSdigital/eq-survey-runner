import QuestionPage from '../question.page'

class ShoeSizePage extends QuestionPage {

  setShoeSize(size) {
    browser.setValue('input[name="what-is-your-shoe-size"]', size)
    return this
  }

}

export default new ShoeSizePage()
