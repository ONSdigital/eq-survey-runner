// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:48:34.607292 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class HouseholdRelationshipsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('household-relationships')
  }

  clickHouseholdRelationshipsAnswerHusbandOrWife() {
    browser.element('[id="household-relationships-answer-1"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerSameSexCivilPartner() {
    browser.element('[id="household-relationships-answer-2"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerPartner() {
    browser.element('[id="household-relationships-answer-3"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerGrandparent() {
    browser.element('[id="household-relationships-answer-4"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerMotherOrFather() {
    browser.element('[id="household-relationships-answer-5"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerStepMotherOrStepFather() {
    browser.element('[id="household-relationships-answer-6"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerSonOrDaughter() {
    browser.element('[id="household-relationships-answer-7"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerStepChild() {
    browser.element('[id="household-relationships-answer-8"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerBrotherOrSister() {
    browser.element('[id="household-relationships-answer-9"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerStepBrotherOrStepSister() {
    browser.element('[id="household-relationships-answer-10"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerGrandchild() {
    browser.element('[id="household-relationships-answer-11"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerRelationOther() {
    browser.element('[id="household-relationships-answer-12"]').click().pause(300)
    return this
  }

  clickHouseholdRelationshipsAnswerUnrelatedIncludingFosterChild() {
    browser.element('[id="household-relationships-answer-13"]').click().pause(300)
    return this
  }

}

export default new HouseholdRelationshipsPage()
