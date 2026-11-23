describe('Pengujian Otentikasi & Login LMS SMAN 10 Garut', () => {

  beforeEach(() => {
    cy.visit('/login');
  });

  it('TC01: Siswa dapat login dengan akun valid (Raesa Gista)', () => {
    cy.get('input[name="username"]').should('be.visible').type('siswa.raesa');
    cy.get('input[name="password"]').should('be.visible').type('siswa12345');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/siswa');
    cy.contains('Raesa Gista').should('be.visible');
  });

  it('TC02: Guru dapat login dengan akun valid (Bu Siti)', () => {
    cy.get('input[name="username"]').should('be.visible').type('guru.siti');
    cy.get('input[name="password"]').should('be.visible').type('guru12345');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/guru');
    cy.contains('Siti Rahmawati').should('be.visible');
  });

  it('TC03: Admin dapat login dengan akun valid', () => {
    cy.get('input[name="username"]').should('be.visible').type('admin');
    cy.get('input[name="password"]').should('be.visible').type('admin12345');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/admin');
    cy.contains('Administrator').should('be.visible');
  });

  it('TC04: Muncul pesan error saat password salah', () => {
    cy.get('input[name="username"]').should('be.visible').type('siswa.raesa');
    cy.get('input[name="password"]').should('be.visible').type('passwordsalah123');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/login');
    cy.contains('Username atau password salah').should('be.visible');
  });

  it('TC05: Muncul pesan error saat username tidak terdaftar', () => {
    cy.get('input[name="username"]').should('be.visible').type('user.tidakada');
    cy.get('input[name="password"]').should('be.visible').type('passwordbebas');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/login');
    cy.contains('Username atau password salah').should('be.visible');
  });

  it('TC06: Halaman terlindungi tidak bisa diakses tanpa login', () => {
    cy.visit('/siswa');
    cy.url().should('include', '/login');
  });

});
