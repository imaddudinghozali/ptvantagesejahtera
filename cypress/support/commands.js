// ***********************************************
// Cypress Custom Commands LMS SMAN 10 Garut
// ***********************************************

Cypress.Commands.add('login', (username, password) => {
  cy.visit('/login');
  cy.get('input[name="username"]').should('be.visible').type(username);
  cy.get('input[name="password"]').should('be.visible').type(password);
  cy.get('button[type="submit"]').click();
});
