import { EventEmitter } from 'events'

import domready from './domready'
import forEach from 'lodash/forEach'
import debounce from 'lodash/debounce'
import delay from 'lodash/delay'

const opts = {
  main: 'js-relationship',
  classItem: 'js-relationship-item',
  classLegend: 'js-relationship-legend',
  classBody: 'js-relationship-body',
  classOpen: 'is-open',
  classClosed: 'is-closed',
  classEditBtn: 'js-relationship-editbtn'
}

class HouseholdRelationship extends EventEmitter {
  constructor(item) {
    super()
    this.el = item
    this.answered = false

    this.editBtn = this.el.querySelector(`.${opts.classEditBtn}`)
    this.editBtn.addEventListener('click', this.onEditBtnClick)

    this.closeLabel = this.editBtn.getAttribute('data-close')
    this.openLabel = this.editBtn.innerHTML

    this.options = this.el.querySelectorAll('input')

    this.optionsContainer = this.el.querySelector(`.${opts.classBody}`)
    this.optionsContainer.addEventListener('keydown', this.onOptionSelected)
    this.optionsContainer.addEventListener('click', this.onOptionSelected)
    this.optionsContainer.addEventListener('change', this.onOptionChanged)

    this.legend = this.el.querySelector(`.${opts.classLegend}`)

    let selection = this.el.querySelector('input:checked')
    if (selection) {
      this.setRelationship(selection.value)
    }
  }

  setRelationship(relationship) {
    this.legend.innerHTML = relationship.toLowerCase()
    this.answered = true
  }

  onFocus = e => {
    this.open()
  }

  onOptionSelected = debounce((e) => {
    if (!this.answered) {
      this.answered = true
    }

    if (e.keyCode === undefined || e.keyCode === 0) {
      this.close()
      this.emit('optionSelected', this)
    }
  }, 100, { leading: true, trailing: false })

  onOptionChanged = (e) => {
    this.setRelationship(e.target.getAttribute('value'))
  }

  onEditBtnClick = (e) => {
    e.preventDefault()
    // remove focus
    if (document.activeElement !== document.body) document.activeElement.blur()
    this.toggle()
    return false
  }

  toggle = () => {
    this.isOpen ? this.close() : this.open()
  }

  open = () => {
    this.isOpen = true
    this.optionsContainer.setAttribute('aria-hidden', false)
    this.el.classList.add(opts.classOpen)
    this.el.classList.remove(opts.classClosed)
    this.editBtn.innerHTML = this.closeLabel
    this.optionsContainer.removeEventListener('focus', this.onFocus, true)
    this.emit('opened', this)
  }

  close = () => {
    if (this.answered) {
      this.editBtn.classList.remove('u-hidden')
    }
    this.isOpen = false
    this.optionsContainer.setAttribute('aria-hidden', true)
    this.el.classList.remove(opts.classOpen)
    this.el.classList.add(opts.classClosed)
    this.editBtn.innerHTML = this.openLabel
    // delay to prevent race conditions
    delay(() => this.optionsContainer.addEventListener('focus', this.onFocus, true), 100)
  }
}

class HouseholdRelationships {

  items = []

  constructor(options) {
    this.el = document.querySelector(`.${opts.main}`)

    if (!this.el) return

    forEach(this.el.getElementsByClassName(opts.classItem), item => {
      const relationship = new HouseholdRelationship(item)
      relationship.addListener('opened', this.onItemOpen)
      relationship.addListener('optionSelected', this.onOptionSelected)
      this.items.push(relationship)
    })

    let firstUnansweredItem = this.items.filter(item => !item.answered)[0]
    if (firstUnansweredItem !== undefined) {
      firstUnansweredItem.open()
    } else {
      this.items.map(item => item.close())
    }
  }

  onOptionSelected = (selectedItem) => {
    const unansweredItems = this.items.filter(item => !item.answered)
    if (unansweredItems.length > 0) {
      unansweredItems[0].open()
    } else {
      selectedItem.close()
    }
  }

  onItemOpen = (item) => {
    this.closeAllExcept(item)
  }

  closeAllExcept(itemToOpen) {
    this.items
      .filter(item => item !== itemToOpen)
      .map(item => item.close())
  }
}

domready(() => {
  new HouseholdRelationships()
})
