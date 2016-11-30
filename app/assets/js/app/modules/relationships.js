import domready from './domready'
import forEach from 'lodash/forEach'

const opts = {
  Main: 'js-relationship',
  classItem: 'js-relationship-item',
  classTrigger: 'js-relationship-trigger',
  classBody: 'js-relationship-body',
  classClosed: 'is-closed',
  classEditBtn: 'js-relationship-editbtn',
  openFirstItem: true
}

class HouseholdRelationshipItem {
  constructor(item, onOpenCallback) {
    this.el = item
    this.onOpenCallback = onOpenCallback
    this.editBtn = this.el.querySelector(`.${opts.classEditBtn}`)
    this.editBtn.addEventListener('click', this.onEditBtnClick)
    this.closeLabel = this.editBtn.getAttribute('data-close')
    this.openLabel = this.editBtn.innerHTML
  }

  onEditBtnClick = (e) => {
    e.preventDefault()
    this.toggle()
    return false
  }

  toggle = () => {
    this.isOpen ? this.close() : this.open()
  }

  close = () => {
    this.isOpen = false
    this.el.setAttribute('aria-hidden', true)
    this.el.classList.add(opts.classClosed)
    this.editBtn.innerHTML = this.openLabel
  }

  open = () => {
    this.isOpen = true
    this.onOpenCallback(this)
    this.el.setAttribute('aria-hidden', false)
    this.el.classList.remove(opts.classClosed)
    this.editBtn.innerHTML = this.closeLabel
  }
}

class HouseholdRelationship {

  items = []

  constructor(options) {
    this.el = document.querySelector(`.${opts.Main}`)

    forEach(this.el.getElementsByClassName(opts.classItem), item => {
      this.items.push(new HouseholdRelationshipItem(item, this.onItemOpen))
    })

    this.items[0].open()
  }

  onItemOpen = (item) => {
    this.closeAllExcept(item)
  }

  closeAllExcept(itemToClose) {
    this.items
      .filter(item => item !== itemToClose)
      .map(item => item.close())
  }
}

domready(() => {
  new HouseholdRelationship()
})
