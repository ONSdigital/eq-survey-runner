import { inPageLink, applyInPageLink, classTrigger, classDetails, attrInputId } from 'app/modules/inpagelink'

const strTemplate = `<div class="panel panel--error">
  <div class="panel__header">
    <div class="panel__title"><h1 class="panel__title venus">This page has 1 errors</h1> </div>
  </div>
  <div class="panel__body">
    <p class="mars">These <strong>must be corrected</strong> to continue.</p>
    <ul class="list list--bare">
        <li class="list__item mars">
          1) <a class="${classTrigger}" href="#ea08f977-33a8-4933-ad7b-c497997107cf">Please provide a value, even if your value is 0.</a>
        </li>
    </ul>
  </div>
</div>
<div class="panel panel--error">
  <div class="panel__header">
    <div class="panel__title">
        <ul class="list list--bare">
          <li class="list__item mars" data-error-msg="Please provide a value, even if your value is 0." data-error="true" data-error-id="7a4b1aee-d6b9-4581-ab18-1191e5ebb94d">Please provide a value, even if your value is 0.</li>
        </ul>
      </div>
  </div>
  <div class="panel__body">
    <div class="field">
      <label class="label " for="ea08f977-33a8-4933-ad7b-c497997107cf" id="label-ea08f977-33a8-4933-ad7b-c497997107cf">
        <span class="label__inner venus">Total retail turnover</span>
      </label>
      <div class="input-type input-type--currency" data-type="£">
        <input class="input input--currency" id="ea08f977-33a8-4933-ad7b-c497997107cf" name="ea08f977-33a8-4933-ad7b-c497997107cf" type="text">
      </div>
    </div>
  </div>
</div>`

let elDetails, elTrigger, elId, elTemplate

describe('In page link', () => {
  before('Add template to DOM', () => {
    let wrapper = document.createElement('div')
    wrapper.innerHTML = strTemplate
    elTemplate = wrapper
    elDetails = elTemplate.getElementsByClassName(classDetails)[0]
    document.body.appendChild(elTemplate)
  })

  it('DOM should contain the template', () => {
    expect(document.body.contains(elTemplate)).to.equal(true)
  })

  it('Input should recieve focus after in page link is clicked', () => {
    const elTrigger = elTemplate.parentElement.getElementsByClassName(classTrigger)[0]
    elTrigger.click()
    expect(document.activeElement.classList.contains("input")).to.equal(true)
  })
})
