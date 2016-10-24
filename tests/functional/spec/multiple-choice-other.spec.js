import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import PizzaToppingsPage from '../pages/surveys/checkbox_other/0/pizza-toppings.page'
import PizzaBasesPage from '../pages/surveys/checkbox_other/0/pizza-bases.page'
import CheckboxOtherSummaryPage from '../pages/surveys/checkbox_other/0/checkbox-other-summary.page'

const expect = chai.expect

describe('Multiple choice "other" option', function() {

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible', function() {
    startQuestionnaire('0_checkbox_other.json')
    browser.click('[data-qa="has-other-option"]')
    expect(browser.isVisible('[data-qa="other-option"]')).to.be.true
  })

  it('Given a non-mandatory checkbox answer, when the user does not select an option, "No answer provided" should be displayed on the summary screen', function() {

     // Given
     startQuestionnaire('0_checkbox_other.json')

     // When
     PizzaToppingsPage.submit();
     expect(PizzaBasesPage.isVisible()).to.be.true
     PizzaBasesPage.setPizzaBase('thin');
     PizzaBasesPage.submit();

     // Then
     expect(CheckboxOtherSummaryPage.getPizzaToppingAnswer()).to.equal('No answer provided')

  })

  it('Given a checkbox answer, when the user selects Other but does not supply a value, "Other" should be displayed on the summary screen', function() {

     // Given
     startQuestionnaire('0_checkbox_other.json')

     // When
     PizzaToppingsPage.selectOther();
     PizzaToppingsPage.submit();

     expect(PizzaBasesPage.isVisible()).to.be.true
     PizzaBasesPage.setPizzaBase('deep pan');
     PizzaBasesPage.submit();

     // Then
     expect(CheckboxOtherSummaryPage.getPizzaToppingAnswer()).to.have.string('Other');

  })

  it('Given a checkbox answer, when the user selects Other and supplies a value, the supplied value should be displayed on the summary screen', function() {

     // Given
     startQuestionnaire('0_checkbox_other.json')

     // When
     PizzaToppingsPage.selectOther();
     PizzaToppingsPage.inputOtherValue('The other value')
     PizzaToppingsPage.submit();

     expect(PizzaBasesPage.isVisible()).to.be.true
     PizzaBasesPage.setPizzaBase('deep pan');
     PizzaBasesPage.submit();

     // Then
     expect(CheckboxOtherSummaryPage.getPizzaToppingAnswer()).to.have.string('The other value');

  })

})
