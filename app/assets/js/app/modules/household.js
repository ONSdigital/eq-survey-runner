import domready from './domready'
import { EventEmitter } from 'events'

class HouseholdMember extends EventEmitter {
  constructor(index) {
    super()
    this.index = index
  }

  bindToExisting(node) {
    this.node = node
    this.removeBtn = this.node.querySelector('.js-btn-remove')
    this.bindToDOM()
  }

  bindToDOM() {
    this.indexNode = this.node.querySelector('.js-household-loopindex')
    const errorNode = this.node.querySelector('.js-has-errors')

    if (errorNode) {
      const fieldNodes = this.node.querySelector('.js-fields')
      if (fieldNodes) {
        errorNode.innerHTML = ''
        errorNode.appendChild(fieldNodes)
      }
    }

    this.inputs = this.node.querySelectorAll('input')
    this.actionNode = this.node.querySelector('.js-household-action')
    if (this.removeBtn) {
      this.removeBtn.addEventListener('click', this.onRemoveClick)
    }
  }

  add(node, parent) {
    this.node = node
    this.removeBtn = document.createElement('button')
    this.bindToDOM(node)
    this.removeTxt = this.node.getAttribute('data-remove')
    this.removeBtn.innerHTML = this.removeTxt
    this.removeBtn.classList.add('btn', 'btn--link')
    this.removeBtn.setAttribute('type', 'button')
    this.node.classList.add('is-hidden')
    this.actionNode.innerHTML = ''
    this.actionNode.appendChild(this.removeBtn)

    parent.appendChild(this.node)
    this.node.querySelector('input').focus()
    this.setIndex(this.index)
    this.inputs.forEach(input => { input.value = '' })
    window.setTimeout(this.node.classList.remove('is-hidden'), 100)
  }

  setIndex(index) {
    this.index = index
    this.indexNode.innerHTML = index
    this.inputs.forEach(input => {
      const id = input.id
      const label = this.node.querySelector(`label[for=${id}]`)
      const newId = `${id}_${index - 1}`
      input.setAttribute('id', newId)
      label.setAttribute('for', newId)
      input.setAttribute('name', `${input.name.split('_')[0]}_${index - 1}`)
    })
  }

  remove() {
    this.node.classList.add('is-removed')
    this.node.addEventListener('transitionend', this.onTransitionHideEnd)
  }

  onTransitionHideEnd = (e) => {
    this.node.remove()
    this.node.removeEventListener('transitionend', this.onTransitionHideEnd)
    this.emit('removed', this)
  }

  onRemoveClick = (e) => {
    e.preventDefault()
    this.remove()
  }
}

domready(() => {
  const existingPeople = document.querySelectorAll('.js-household-person')
  const btn = document.querySelector('.js-household-btn')
  const householdMembers = []

  if (existingPeople.length === 0) {
    return
  }

  const createHouseholdMember = () => {
    const householdMember = new HouseholdMember(householdMembers.length + 2)
    householdMember.addListener('removed', onRemove)
    householdMembers.push(householdMember)
    return householdMember
  }

  const onRemove = (removedMember) => {
    householdMembers.splice(householdMembers.indexOf(removedMember), 1)
    removedMember.removeListener('removed', onRemove)
    householdMembers.map((member, index) => {
      member.setIndex(index + 2)
    })
  }

  const onAddBtnClick = (e) => {
    e.preventDefault()
    const originalNode = existingPeople[0]
    const newNode = originalNode.cloneNode(true)
    const parent = originalNode.parentNode
    createHouseholdMember().add(newNode, parent)
  }

  existingPeople.forEach((person, index) => {
    if (index > 0) {
      createHouseholdMember().bindToExisting(person)
    }
  })

  btn.setAttribute('type', 'button')
  btn.addEventListener('click', onAddBtnClick)
})
