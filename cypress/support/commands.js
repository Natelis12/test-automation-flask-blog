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
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

// Cypress.Commands.add('registerNewUser',() => {
//   const { username, password, email } = generateUser()

//     cy.request('POST', '/user', {
//       email,
//       password,
//       username
//     }).then(response => response.body.user)

// })

// Cypress.on('uncaught:exception', (err, runnable) => {
//   returning false here prevents Cypress from
//   failing the test
//   return false
// })
// Replace this class-based initialization
// <div class="ck ck-content ck-editor__editable ...">
// import 'cypress-real-events/support';


