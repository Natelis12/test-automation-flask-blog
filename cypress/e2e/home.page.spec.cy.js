/// <reference types="cypress"/>

describe('My Home page', () => {
  beforeEach(() => {
    cy.visit('/');
  })

  it('should have main parts', () => {
    cy.get('h1')
    .should('contain.text', 'flaskBlog');

    cy.contains('a', 'Cool blog')
    .should('exist');

    cy.contains('p', 'Blah blah blah')
    .should('exist');

    cy.contains('a', 'read more')
    .should('exist');

    cy.contains('button', '🌞')
    .should('exist');
  })

    it('should click on Login', () => {

      cy.contains('a', 'Login')
      .should('exist').click();

      cy.url().should('include', '/login')
      cy.get('h1').should('contain.text', 'flaskBlog')

      
      cy.contains('button', '🌞').click();
    });

  it('should click on Sign Up', () => {

    cy.contains('a', 'Sign Up')
    .should('exist').click();

    cy.url().should('include', '/signup')
    cy.get('h1').should('contain.text', 'flaskBlog')
  });
})
    //cy.contains('read more').click();

    //cy.contains('Sign Up').click();
    //cy.contains('Login').click();
    //cy.get('h1').should('contain.text', 'Login')
