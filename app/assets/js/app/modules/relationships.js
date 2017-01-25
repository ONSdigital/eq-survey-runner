import { EventEmitter } from 'events'

import domready from './domready'

import {forEach, debounce, delay} from 'lodash'
const opts = {
  main: 'js-relationship',
  classItem: 'js-relationship-item',
  classLegend: 'js-relationship-legend',
  classBody: 'js-relationship-body',
  classTrigger: 'js-relationship-trigger',
  classOpen: 'is-open',
  classClosed: 'is-closed',
  classEditBtn: 'js-relationship-editbtn'
}

class HouseholdRelationship extends EventEmitter {
  constructor(item) {
    super()
    this.el = item
    this.answered = false

    this.name = this.el.getAttribute('data-relationship-name')

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
      this.setRelationship(selection.id)
    }
  }

  setRelationship(relationshipId) {
    const label = this.el.querySelector('label[for=' + relationshipId + ']')
    const relationship = label.innerHTML

    this.legend.innerHTML = relationship.toLowerCase()
    this.answered = true
  }

  onFocus = e => {
    this.open(true)
  }

  onOptionSelected = debounce((e) => {
    if (!this.answered) {
      this.answered = true
    }

    if (e.target.classList.contains(opts.classTrigger) && (e.keyCode === undefined || e.keyCode === 0)) {
      this.emit('optionSelected', this)
    }
  }, 100, { leading: true, trailing: false })

  onOptionChanged = (e) => {
    this.setRelationship(e.target.getAttribute('id'))
  }

  onEditBtnClick = (e) => {
    e.preventDefault()
    this.toggle()
    return false
  }

  toggle = () => {
    this.isOpen ? this.close(true) : this.open(true)
  }

  open = (emitEvent) => {
    this.isOpen = true
    this.optionsContainer.setAttribute('aria-hidden', false)
    this.el.classList.add(opts.classOpen)
    this.el.classList.remove(opts.classClosed)
    this.editBtn.innerHTML = this.closeLabel
    this.optionsContainer.removeEventListener('focus', this.onFocus, true)
    if (emitEvent) {
      this.emit('opened', this)
    }
  }

  close = (emitEvent) => {
    if (this.answered) {
      this.editBtn.classList.remove('u-hidden')
    }
    this.isOpen = false
    this.optionsContainer.setAttribute('aria-hidden', true)
    this.el.classList.remove(opts.classOpen)
    this.el.classList.add(opts.classClosed)
    this.editBtn.innerHTML = this.openLabel
    // delay to prevent race conditions
    delay(() => {
      this.optionsContainer.addEventListener('focus', this.onFocus, true)
    }, 100)
    if (emitEvent) {
      this.emit('closed', this)
    }
  }
}

domready(() => {
  const items = []
  const el = document.querySelector(`.${opts.main}`)

  if (!el) return

  const onOptionSelected = (selectedItem) => {
    selectedItem.close(true)
  }

  const onItemOpen = (itemOpened) => {
    items.forEach(item => {
      if (item.isOpen && item !== itemOpened) {
        item.close(false)
      }
    })
  }

  const onItemClosed = (itemClosed) => {
    openNextUnanswered()
  }

  const openNextUnanswered = () => {
    let next = items.filter(item => !item.answered)[0]
    if (next !== undefined) {
      next.open(true)
    }
  }

  forEach(el.getElementsByClassName(opts.classItem), item => {
    const relationship = new HouseholdRelationship(item)
    relationship.addListener('opened', onItemOpen)
    relationship.addListener('closed', onItemClosed)
    relationship.addListener('optionSelected', onOptionSelected)
    items.push(relationship)
  })

  let firstUnansweredItem = items.filter(item => !item.answered)[0]
  items.forEach(item => {
    if (item !== firstUnansweredItem) {
      item.close(false)
    } else {
      item.open(false)
    }
  })
})
