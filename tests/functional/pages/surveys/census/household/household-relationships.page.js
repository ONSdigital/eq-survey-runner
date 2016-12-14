// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.728571 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class HouseholdRelationshipsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('household-relationships')
  }

  clickHouseholdRelationshipsAnswerHusbandOrWife() {
    browser.element('[id="household-relationships-answer-1"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerSameSexCivilPartner() {
    browser.element('[id="household-relationships-answer-2"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerPartner() {
    browser.element('[id="household-relationships-answer-3"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerGrandparent() {
    browser.element('[id="household-relationships-answer-4"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerMotherOrFather() {
    browser.element('[id="household-relationships-answer-5"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerStepMotherOrStepFather() {
    browser.element('[id="household-relationships-answer-6"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerSonOrDaughter() {
    browser.element('[id="household-relationships-answer-7"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerStepChild() {
    browser.element('[id="household-relationships-answer-8"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerBrotherOrSister() {
    browser.element('[id="household-relationships-answer-9"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerStepBrotherOrStepSister() {
    browser.element('[id="household-relationships-answer-10"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerGrandchild() {
    browser.element('[id="household-relationships-answer-11"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerRelationOther() {
    browser.element('[id="household-relationships-answer-12"]').click()
    return this
  }

  clickHouseholdRelationshipsAnswerUnrelatedIncludingFosterChild() {
    browser.element('[id="household-relationships-answer-13"]').click()
    return this
  }

}

export default new HouseholdRelationshipsPage()
