import charLimit, { inputClass, msgClass, msgLabel, attrRemainingMsg, attrMaxLength, applyCharLimit } from 'app/modules/charlimit'

let elTemplate, inputInstance, msgEl, nodes

const limit = 20

const strTemplate = `
  <textarea class="${inputClass}" data-maxlength="${limit}"></textarea>
  <div class="${msgLabel}" ${attrRemainingMsg}="Characters remaining">Maximum characters</div>:
  <div class="${msgClass}">${limit}</div>
`

describe('Character Limit', function() {
  before('Add template to DOM', function() {
    let wrapper = document.createElement('div')
    wrapper.innerHTML = strTemplate
    elTemplate = wrapper
    document.body.appendChild(elTemplate)

    inputInstance = document.getElementsByClassName(inputClass)[0]
    msgEl = document.getElementsByClassName(msgClass)[0]
    nodes = charLimit()
  })

  it('should return a nodeList with a length of 1', function() {
    expect(nodes.length).to.equal(1)
  })

  it('should render limit in to msg element', function() {
    expect(msgEl.innerText).to.equal(limit.toString())
  })

  it('should decrease the limit message by the number of characters entered', function() {
    const testString = 'test!!!'
    inputInstance.value = testString
    const newValue = applyCharLimit(inputInstance.value, limit)
    expect(limit - newValue.length).to.equal(limit - testString.length)
  })

  it('should prevent excess characters being entered', function() {
    const testString = '123'
    inputInstance.value = testString
    let length = applyCharLimit(inputInstance.value, 1).length
    expect(length).to.equal(1)
  })
})
