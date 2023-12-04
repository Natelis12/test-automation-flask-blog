describe('Login page', () => {
  beforeEach(() => {
  cy.visit('/login/redirect=&');
})

  it('should be allow to login', () => {
    cy.get('h2').should('contain.text', 'Login')
    cy.get('#userName').type('test_user_892062774735608');
    cy.get('#password').type('password123');
    cy.get('.form > .btn').click()
    
    cy.get('#flash').should('contain.text', 'Welcome test_user_892062774735608')
    });
  })

    it.skip('should not be allow to login', () => {
      cy.get('h2').should('contain.text', 'Login')
      cy.get('#userName').type('test_user_2062774735608');
      cy.get('#password').type('password123');
      cy.get('.form > .btn').click()
      
      cy.get('#flash').should('contain.text', 'user not found')

    });
  //})