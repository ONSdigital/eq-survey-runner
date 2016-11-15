import QuestionPage from '../question.page'

class HouseholdCompositionPage extends QuestionPage {

  setPersonName(id, value) {
    var field = "414699da-1667-44fd-8e98-7606966884db"
    if (id > 0) {
        field = field + "_" + id
    }
    browser.setValue('input[name="' + field + '"]', value)
    return this
  }

}

export default new HouseholdCompositionPage()
