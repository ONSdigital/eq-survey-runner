import charLimit, { inputClass, msgClass, maxLengthAttr, applyCharLimit } from 'app/modules/charlimit'

describe('charlimit', () => {
  const msgClass = 'js-charlimit-msg'
  const textEl = document.createElement('textarea')
  const msgEl = document.createElement('div')
  const parentEl = document.createElement('div')

  const limit = 20

  textEl.classList.add(inputClass)
  textEl.setAttribute(maxLengthAttr, limit)

  msgEl.classList.add(msgClass)

  parentEl.appendChild(textEl)
  parentEl.appendChild(msgEl)

  document.body.appendChild(parentEl)

  const inputInstance = document.getElementsByClassName(inputClass)
  const msgInstance = document.getElementsByClassName(msgClass)

  const nodes = charLimit()

  it('should return a nodeList with a length of 1', () => {
    expect(nodes.length).to.equal(1)
  })

  it('should render limit in to msg element', () => {
    expect(msgEl.innerText).to.equal(limit.toString())
  })

  it('should decrease the limit message by the number of characters entered', () => {
    const testString = 'test!!!'
    inputInstance.value = testString
    const newValue = applyCharLimit(inputInstance.value, limit)
    expect(limit - newValue.length).to.equal(limit - testString.length)
  })

  it('should prevent excess characters being entered', () => {
    const testString = '123'
    inputInstance.value = testString
    let length = applyCharLimit(inputInstance.value, 1).length
    expect(length).to.equal(1)
  })
})
