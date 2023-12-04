describe('Sign up page', () => {
  beforeEach(() => {
cy.visit('/signup');
  })
  const randomNumber = Math.random().toString().slice(2);
  const userName = `test_user_${randomNumber}`
  const email = `${userName}@gmail.com`;

it('should register user', () => {
cy.get('h2')
.should('contain.text', 'Sign Up')

cy.get('#userName').type(userName);
cy.get('#email').type(email);
cy.get('#password').type('password123');
cy.get('#passwordConfirm').type('password123');
cy.get('.form > .btn').click();

cy.url().should('equal', Cypress.config().baseUrl)

  });

  it('should not allow register with an existed email ', () => {

    cy.get('h2').should('contain.text', 'Sign Up')

    cy.get('#userName').type(userName + '_new');
    cy.get('#email').type(email);
    cy.get('#password').type('password123');
    cy.get('#passwordConfirm').type('password123');
    cy.get('.form > .btn').click();

  cy.get('#flash').should('contain.text', 'This username and email is unavailable.')
});
});