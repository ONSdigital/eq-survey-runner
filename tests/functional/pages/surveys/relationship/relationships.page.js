// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class RelationshipsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('relationships')
  }

  clickWhoIsRelatedHusbandOrWife(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Husband or wife')
    return this
  }

  clickWhoIsRelatedPartner(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Partner')
    return this
  }

  clickWhoIsRelatedMotherOrFather(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Mother or father')
    return this
  }

  clickWhoIsRelatedSonOrDaughter(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Son or daughter')
    return this
  }

  clickWhoIsRelatedBrotherOrSister(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Brother or sister')
    return this
  }

  clickWhoIsRelatedRelationOther(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Relation - other')
    return this
  }

  clickWhoIsRelatedGrandparent(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Grandparent')
    return this
  }

  clickWhoIsRelatedGrandchild(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Grandchild')
    return this
  }

  clickWhoIsRelatedUnrelated(instance = 0) {
    browser.selectByValue('[id="who-is-related-' + instance + '"]', 'Unrelated')
    return this
  }

}

export default new RelationshipsPage()
