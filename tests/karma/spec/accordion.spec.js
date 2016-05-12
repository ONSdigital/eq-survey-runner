import accordion, {classAccordion, classAccordionItem, classAccordionTrigger, classAccordionBody, classClosed} from 'app/modules/accordion'

export const attrHidden = 'aria-hidden'

const strTemplate = `
<div class="accordion ${classAccordion}">
  <div class="accordion__item ${classAccordionItem}">
    <button class="accordion__head ${classAccordionTrigger}">
      <h3 class="accordion__title">How is your information used?</h3>
    </button>
    <div class="accordion__body ${classAccordionBody}">
      <p>Sed posuere consectetur est at lobortis. Donec sed odio dui. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id dolor id nibh ultricies vehicula ut id elit.</p>
    </div>
  </div>
</div>`

let elTemplate

describe('Accordion', () => {
  before('Add template to DOM', () => {
    let wrapper = document.createElement('div')
    wrapper.innerHTML = strTemplate
    elTemplate = wrapper
    document.body.appendChild(elTemplate)
    accordion()
  })

  it('DOM should contain the template', () => {
    expect(document.body.contains(elTemplate)).to.equal(true)
  })

  it(`Should toggle class '.${classClosed}' when clicked`, () => {
    const elTrigger = elTemplate.parentElement.getElementsByClassName(classAccordionTrigger)[0]
    const elAccordionItem = elTemplate.parentElement.getElementsByClassName(classAccordionItem)[0]

    elTrigger.click()
    expect(elAccordionItem.classList.contains(classClosed)).to.equal(false)

    elTrigger.click()
    expect(elAccordionItem.classList.contains(classClosed)).to.equal(true)
  })
})
