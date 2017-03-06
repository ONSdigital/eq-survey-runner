// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class RelationshipsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('relationships')
  }

  setWhoIsRelatedHusbandOrWife(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Husband or wife')
    return this
  }

  setWhoIsRelatedPartner(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Partner')
    return this
  }

  setWhoIsRelatedMotherOrFather(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Mother or father')
    return this
  }

  setWhoIsRelatedSonOrDaughter(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Son or daughter')
    return this
  }

  setWhoIsRelatedBrotherOrSister(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Brother or sister')
    return this
  }

  setWhoIsRelatedRelationOther(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Relation - other')
    return this
  }

  setWhoIsRelatedGrandparent(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Grandparent')
    return this
  }

  setWhoIsRelatedGrandchild(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Grandchild')
    return this
  }

  setWhoIsRelatedUnrelated(instance = 0) {
    browser.selectByValue('[name="who-is-related-' + instance + '"]', 'Unrelated')
    return this
  }

}

export default new RelationshipsPage()
