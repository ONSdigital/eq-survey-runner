// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

// Gets the text content from an element using the jQuery 'text' function and trim the output
// Optional argument of 'stripNewlines' to remove newlines from the text output.
Cypress.Commands.add('stripText', { prevSubject: true }, (subject, stripNewlines) => {
  return cy.wrap(subject).invoke('text').then((text) => {
    if (stripNewlines === true) {
      text = text.replace(/\n/g, '')
    }
    return text.trim()
  })
})

// Force typing even though the subject may be covered by another element.
// This happens with unit types.
Cypress.Commands.add('typeForced', { prevSubject: true }, (subject, textToType) => {
  return cy.wrap(subject).type(textToType, {force: true})
})

Cypress.Commands.add('key', (subject, keyCode) => {
  cy.focused().trigger('keydown', {
      keyCode: keyCode,
      which: keyCode,
  });
});
