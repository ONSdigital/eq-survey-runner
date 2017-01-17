// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class HouseholdRelationshipsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('household-relationships')
  }

  clickHouseholdRelationshipsAnswerHusbandOrWife(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-0"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerSameSexCivilPartner(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-1"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerPartner(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-2"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerGrandparent(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-3"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerMotherOrFather(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-4"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerStepMotherOrStepFather(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-5"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerSonOrDaughter(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-6"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerStepChild(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-7"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerBrotherOrSister(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-8"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerStepBrotherOrStepSister(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-9"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerGrandchild(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-10"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerRelationOther(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-11"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerUnrelatedIncludingFosterChild(instance = 0) {
    browser.element('[id="household-relationships-answer-' + instance + '-12"]').click().pause(300)
    return this
  }

}

export default new HouseholdRelationshipsPage()
