import domready from './domready'

class HouseholdMember {
  constructor(people, index, onRemove) {
    this.onRemoveCallback = onRemove
    this.node = people[people.length - 1].cloneNode(true)
    this.indexNode = this.node.querySelector('.js-household-loopindex')
    const errorNode = this.node.querySelector('.js-has-errors')

    if (errorNode) {
      const fieldNodes = this.node.querySelector('.js-fields')
      if (fieldNodes) {
        errorNode.innerHTML = ''
        errorNode.appendChild(fieldNodes)
      }
    }

    // create a new ID and apply to all inputs/labels
    this.inputs = this.node.querySelectorAll('input')
    this.inputs.forEach(input => { input.value = '' })

    this.setIndex(index)

    this.parent = people[0].parentNode
    this.actionNode = this.node.querySelector('.js-household-action')

    this.removeBtn = document.createElement('button')
    this.removeBtn.innerHTML = 'remove'
    this.removeBtn.classList.add('btn', 'btn--link')
    this.removeBtn.addEventListener('click', this.onRemoveClick)

    this.node.classList.add('is-hidden')
    this.actionNode.innerHTML = ''
    this.actionNode.appendChild(this.removeBtn)
  }

  setIndex(index) {
    this.indexNode.innerHTML = index
    this.inputs.forEach(input => {
      const id = input.id
      const label = this.node.querySelector(`label[for=${id}]`)
      const newId = `${id}-${index}`
      input.setAttribute('id', newId)
      label.setAttribute('for', newId)
    })
  }

  add() {
    this.parent.appendChild(this.node)
    this.node.querySelector('input').focus()
    window.setTimeout(this.node.classList.remove('is-hidden'), 100)
  }

  remove() {
    this.node.classList.add('is-removed')
    this.node.addEventListener('transitionend', this.onTransitionHideEnd)
  }

  onTransitionHideEnd = (e) => {
    this.node.remove()
    this.node.removeEventListener('transitionend', this.onTransitionHideEnd)
    this.onRemoveCallback(this)
  }

  onRemoveClick = (e) => {
    e.preventDefault()
    this.remove()
  }
}

domready(() => {
  const btn = document.querySelector('.js-household-btn')
  let householdMembers = []

  const onRemove = (removedMember) => {
    householdMembers.splice(householdMembers.indexOf(removedMember), 1)
    householdMembers.map((member, index) => {
      console.log(member)
      member.setIndex(index + 1)
    })
  }

  const onAddBtnClick = (e) => {
    const people = document.querySelectorAll('.js-household-person')
    const householdMember = new HouseholdMember(people, householdMembers.length + 1, onRemove)
    e.preventDefault()
    householdMember.add()
    householdMembers.push(householdMember)
  }

  btn.addEventListener('click', onAddBtnClick)
})
