describe('Login page', () => {
  beforeEach(() => {
  cy.visit('/login/redirect=&');
})

  it('should have aacess to settings', () => {
    cy.get('h2').should('contain.text', 'Login')
    cy.get('#userName').type('test_user_892062774735608');
    cy.get('#password').type('qwerty123');
    cy.get('.form > .btn').click()

    cy.visit('/user/test_user_892062774735608');
    cy.get('[href="/accountsettings"]').click()
    cy.get(':nth-child(2) > .toPanel').click()

    cy.get('#oldPassword').type('qwerty');
    cy.get('#password').type('password123');
    cy.get('#passwordConfirm').type('password123')
    cy.get('.form > .btn').click()
    cy.get('#flash').should('contain.text', 'old password wrong')

    cy.get('#oldPassword').type('qwerty123');



    //cy.get('#flash').should('contain.text', 'you need to login with new password')

    });
  })


  //})