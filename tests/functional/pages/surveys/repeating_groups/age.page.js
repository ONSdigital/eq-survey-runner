import QuestionPage from '../question.page'

class AgePage extends QuestionPage {

  setAge(age) {
    browser.setValue('input[name="what-is-your-age"]', age)
    return this
  }

}

export default new AgePage()
