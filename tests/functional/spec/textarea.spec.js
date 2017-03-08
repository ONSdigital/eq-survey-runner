import {openQuestionnaire} from '../helpers'

import TextareaBlock from '../pages/surveys/answers/textarea-block.page.js'
import TextareaSummary from '../pages/surveys/answers/textarea-summary.page.js'

describe('Textarea', function() {

  it('Given a textarea option, a user should be able to click the label of the textarea to focus', function() {
    openQuestionnaire('test_textarea.json')
    TextareaBlock.getAnswerLabel().click()
    expect(browser.hasFocus(TextareaBlock.getAnswerElement().selector)).to.be.true
  })

  it('Given a textarea option, When no text is entered, Then the summary should display "No answer provided"', function() {
    openQuestionnaire('test_textarea.json')
    TextareaBlock.submit()
    expect(TextareaSummary.getAnswer()).to.contain('No answer provided')
  })

  it('Given a textarea option, When some text is entered, Then the summary should display the text', function() {
    openQuestionnaire('test_textarea.json')
    TextareaBlock.setAnswer('Some text').submit()
    expect(TextareaSummary.getAnswer()).to.contain('Some text')
  })

})
