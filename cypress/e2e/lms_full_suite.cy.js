describe('Suite Pengujian Otomatis LMS SMAN 10 Garut (Total 20 Test Cases: 15 Berhasil + 5 Gagal)', () => {

  // =========================================================================
  // BAGIAN 1: UI TESTING - OTENTIKASI & KEAMANAN AKSES (TC01 - TC06) [PASSED]
  // =========================================================================
  context('Otentikasi & Keamanan Hak Akses (Lolos / Passed)', () => {

    it('TC01: Siswa dapat login dengan kredensial valid (Raesa Gista)', () => {
      cy.login('siswa.raesa', 'siswa12345');
      cy.url().should('include', '/siswa');
      cy.contains('Raesa Gista').should('be.visible');
    });

    it('TC02: Guru dapat login dengan kredensial valid (Siti Rahmawati)', () => {
      cy.login('guru.siti', 'guru12345');
      cy.url().should('include', '/guru');
      cy.contains('Siti Rahmawati').should('be.visible');
    });

    it('TC03: Admin dapat login dengan kredensial valid', () => {
      cy.login('admin', 'admin12345');
      cy.url().should('include', '/admin');
      cy.contains('Administrator').should('be.visible');
    });

    it('TC04: Muncul pesan error saat login dengan password salah', () => {
      cy.login('siswa.raesa', 'passwordsalah123');
      cy.url().should('include', '/login');
      cy.contains('Username atau password salah').should('be.visible');
    });

    it('TC05: Muncul pesan error saat login dengan username tidak terdaftar', () => {
      cy.login('user.fiktif', 'passwordsalah');
      cy.url().should('include', '/login');
      cy.contains('Username atau password salah').should('be.visible');
    });

    it('TC06: Halaman terlindungi tidak dapat diakses tanpa autentikasi (Guest Guard)', () => {
      cy.visit('/siswa');
      cy.url().should('include', '/login');
    });

  });

  // =========================================================================
  // BAGIAN 2: UI TESTING - FITUR UTAMA & KONTEN LMS (TC07 - TC10) [PASSED]
  // =========================================================================
  context('Fitur Utama Portal & Sesi Pengguna (Lolos / Passed)', () => {

    beforeEach(() => {
      // Login sebagai siswa sebelum pengujian fitur portal siswa
      cy.login('siswa.raesa', 'siswa12345');
      cy.url().should('include', '/siswa');
    });

    it('TC07: Memverifikasi Card Integrasi Google Meet di Dashboard Siswa', () => {
      cy.get('a[href*="/siswa/meet"]').should('exist');
      cy.contains('Google Meet').should('be.visible');
    });

    it('TC08: Memverifikasi Papan Peringkat (Leaderboard) dan Ranking Siswa', () => {
      cy.visit('/siswa/pencapaian');
      cy.url().should('include', '/siswa/pencapaian');
      cy.contains('Papan Peringkat').should('be.visible');
      cy.contains('Raesa Gista').should('be.visible');
    });

    it('TC09: Memverifikasi Halaman dan Katalog E-Perpustakaan Digital', () => {
      cy.visit('/perpustakaan');
      cy.url().should('include', '/perpustakaan');
      cy.contains('Perpustakaan Digital SMAN 10 Garut').should('be.visible');
    });

    it('TC10: Pengguna dapat mengakhiri sesi pembelajaran (Logout)', () => {
      // Submit form logout ber-CSRF
      cy.get('#logoutFormAction').submit();
      cy.url().should('include', '/login');
      // Verifikasi sesi terhapus dengan mencoba mengakses /siswa kembali
      cy.visit('/siswa');
      cy.url().should('include', '/login');
    });

  });

  // =========================================================================
  // BAGIAN 3: API TESTING - REST ENDPOINTS & INTEGRASI DATA (TC11 - TC15) [PASSED]
  // =========================================================================
  context('REST API Automation & Data Integrity (Lolos / Passed)', () => {

    it('TC11: [API] GET /api/status - Status operasional API online (HTTP 200)', () => {
      cy.request('GET', '/api/status').then((res) => {
        expect(res.status).to.eq(200);
        expect(res.headers['content-type']).to.include('application/json');
        expect(res.body).to.have.property('ok', true);
        expect(res.body).to.have.property('status', 'online');
        expect(res.body).to.have.property('app', 'LMS SMAN 10 Garut API');
      });
    });

    it('TC12: [API] GET /api/meet/aktif - Mengembalikan daftar sesi Google Meet', () => {
      cy.request('GET', '/api/meet/aktif').then((res) => {
        expect(res.status).to.eq(200);
        expect(res.headers['content-type']).to.include('application/json');
        expect(res.body).to.have.property('ok', true);
        expect(res.body).to.have.property('data');
        expect(res.body.data).to.be.an('array');
      });
    });

    it('TC13: [API] GET /api/leaderboard/1 - Mengembalikan peringkat leaderboard kelas', () => {
      cy.request('GET', '/api/leaderboard/1').then((res) => {
        expect(res.status).to.eq(200);
        expect(res.headers['content-type']).to.include('application/json');
        expect(res.body).to.have.property('ok', true);
        expect(res.body).to.have.property('kelas_id', 1);
        expect(res.body.data).to.be.an('array');
      });
    });

    it('TC14: [API] GET /api/perpustakaan - Mengembalikan katalog buku e-perpustakaan', () => {
      cy.request('GET', '/api/perpustakaan').then((res) => {
        expect(res.status).to.eq(200);
        expect(res.headers['content-type']).to.include('application/json');
        expect(res.body).to.have.property('ok', true);
        expect(res.body).to.have.property('data');
        expect(res.body.data).to.be.an('array');
      });
    });

    it('TC15: [API] GET /api/jadwal/1 - Mengembalikan jadwal mata pelajaran kelas', () => {
      cy.request('GET', '/api/jadwal/1').then((res) => {
        expect(res.status).to.eq(200);
        expect(res.headers['content-type']).to.include('application/json');
        expect(res.body).to.have.property('ok', true);
        expect(res.body).to.have.property('kelas_id', 1);
        expect(res.body.data).to.be.an('array');
      });
    });

  });

  // =========================================================================
  // BAGIAN 4: SIMULASI KEGAGALAN / DEFECT DETECTION (TC16 - TC20) [FAILED]
  // Pengujian yang sengaja dibuat gagal untuk membuktikan ketajaman asersi Cypress
  // =========================================================================
  context('Simulasi Kegagalan Pengujian & Defect Detection (Gagal / Failed)', () => {

    it('TC16: [FAIL] Ekspektasi pesan validasi kompleks yang tidak disediakan form login', () => {
      // Menguji validasi custom spesifik yang sengaja tidak ada pada sistem
      cy.visit('/login');
      cy.get('button[type="submit"]').click();
      cy.contains('Password wajib diisi minimal 8 karakter dan mengandung simbol unik').should('be.visible');
    });

    it('TC17: [FAIL] Ekspektasi siswa diizinkan mengakses halaman panel manajemen admin', () => {
      // Menguji celah eskalasi peran: Siswa mengakses /admin/pengguna
      // Test ini GAGAL karena sistem LMS memblokir siswa (akses ditolak 403 / redirect)
      cy.login('siswa.raesa', 'siswa12345');
      cy.visit('/admin/pengguna', { failOnStatusCode: false });
      cy.contains('Kelola Data Seluruh Pengguna Sekolah').should('be.visible');
    });

    it('TC18: [FAIL] Ekspektasi siswa fiktif terdaftar pada daftar Leaderboard', () => {
      // Mengharapkan entri user fiktif muncul di tabel peringkat kelas
      cy.login('siswa.raesa', 'siswa12345');
      cy.visit('/siswa/pencapaian');
      cy.contains('Siswa Fiktif Tidak Nyata').should('be.visible');
    });

    it('TC19: [FAIL] [API] Ekspektasi endpoint rahasia non-eksis menghasilkan status 200 OK', () => {
      // Menguji endpoint yang tidak pernah dibuat, mengekspektasikan status 200
      // Test ini GAGAL karena backend mengembalikan HTTP 404 Not Found
      cy.request({ url: '/api/data-rahasia-sekolah', failOnStatusCode: false }).then((res) => {
        expect(res.status).to.eq(200);
      });
    });

    it('TC20: [FAIL] [API] Ekspektasi versi API backend sesuai dengan rilis versi v2.5.0', () => {
      // Menguji kesesuaian versi: mengharapkan v2.5.0 padahal backend merespons v1.0.0
      cy.request('GET', '/api/status').then((res) => {
        expect(res.body.version).to.eq('2.5.0');
      });
    });

  });

});
