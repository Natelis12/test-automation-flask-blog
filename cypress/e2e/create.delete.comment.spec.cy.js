describe('Login page', () => {
  beforeEach(() => {
  cy.visit('/login/redirect=&');
})

  it('should create post', () => {
    cy.get('#userName').type('test_user_892062774735608');
    cy.get('#password').type('password123');
    cy.get('.form > .btn').click()
    cy.get('[href="/"] > .btn').should('contain.text', 'flaskBlog');

    cy.get('.post').should('have.length', 3);
    cy.get(':nth-child(9) > .title').click()

    //cy.get('#comment').type('Have a nice day!')
    //cy.get('.btnSubmit').click();
    cy.get('[href="/deletecomment/4/redirect=post&8"]').click()



  })
});








