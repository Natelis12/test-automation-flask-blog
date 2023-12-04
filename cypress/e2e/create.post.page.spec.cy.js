describe('Login page', () => {
  beforeEach(() => {
  cy.visit('/login/redirect=&');
})

  it('should create post', () => {
    cy.get('#userName').type('test_user_892062774735608');
    cy.get('#password').type('password123');
    cy.get('.form > .btn').click()
    cy.get('[href="/"] > .btn').should('contain.text', 'flaskBlog');

    cy.get('[href="/createpost"] > .btn').should('contain.text', 'New Post').click()
    cy.get('[placeholder="post title"]').as('post title');
    cy.get('#postTitle').type('Good morning');
    cy.get('[placeholder="tags"]').as('post title');
    cy.get('#postTags').type('#test');

    cy.get('.ck-editor__editable').then(($editable) => {
      // @ts-ignore
      const editor = $editable[0].ckeditorInstance;
      editor.setData('Hello, this is a test test text.');
    });

    cy.get('.form > .btn').click();
    cy.get('#flash').should('contain.text', 'You earned 20 points by posting');
    cy.get(':nth-child(10) > .title').click()
    cy.get('[href="/deletepost/9/redirect=&"]').click()

    //cy.url().should('include', '/post/');
    //cy.get('h1').should('contain.text', 'Test title');
      });

  })

