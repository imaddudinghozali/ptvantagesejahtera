# Dokumentasi Pengujian Otomatis (Automation Testing) - Cypress
## LMS SMAN 10 Garut (Total 20 Test Cases: 15 Lolos + 5 Gagal)

**Tools & Framework:** Cypress v16.x  
**File Skrip Uji:** `cypress/e2e/lms_full_suite.cy.js`  
**Base URL:** `http://localhost/ptvantagesejahtera-main/public`  
**Hasil Uji yang Ditargetkan:** **15 Passed**, **5 Failed** (Total 20 Kasus Uji)

---

### A. Tabel Matriks 15 Test Cases Berhasil (Passed)

| No | Kode TC | Tipe Uji | Modul / Skenario | Input / Endpoint | Hasil yang Diharapkan (Expected Result) | Status |
|---|---|---|---|---|---|:---:|
| 1 | **TC01** | UI / E2E | Login Siswa Valid | `siswa.raesa` / `siswa12345` | Redirect ke `/siswa`, nama "Raesa Gista" tampil | **PASSED** |
| 2 | **TC02** | UI / E2E | Login Guru Valid | `guru.siti` / `guru12345` | Redirect ke `/guru`, nama "Siti Rahmawati" tampil | **PASSED** |
| 3 | **TC03** | UI / E2E | Login Admin Valid | `admin` / `admin12345` | Redirect ke `/admin`, nama "Administrator" tampil | **PASSED** |
| 4 | **TC04** | UI / E2E | Validasi Password Salah | `siswa.raesa` / `passwordsalah123` | Tetap di `/login`, alert "Username atau password salah" muncul | **PASSED** |
| 5 | **TC05** | UI / E2E | Validasi Akun Tak Terdaftar | `user.fiktif` / `passwordsalah` | Tetap di `/login`, alert "Username atau password salah" muncul | **PASSED** |
| 6 | **TC06** | UI / E2E | Proteksi Hak Akses (Guest Guard) | Buka URL `/siswa` tanpa sesi | Akses ditolak, otomatis redirect (302) kembali ke `/login` | **PASSED** |
| 7 | **TC07** | UI / E2E | Fitur Sesi Google Meet | Navigasi Dashboard Siswa | Elemen menu Google Meet dan sesi daring terdeteksi | **PASSED** |
| 8 | **TC08** | UI / E2E | Leaderboard & Ranking Siswa | Kunjungi `/siswa/pencapaian` | Judul "Papan Peringkat" tampil dan nama "Raesa Gista" terdaftar | **PASSED** |
| 9 | **TC09** | UI / E2E | Katalog E-Perpustakaan | Kunjungi `/perpustakaan` | Judul "Perpustakaan Digital SMAN 10 Garut" dan katalog buku tampil | **PASSED** |
| 10 | **TC10** | UI / E2E | Terminasi Sesi (Logout) | Submit form logout ber-CSRF | Sesi terhapus, redirect `/login`, akses ke `/siswa` diblokir | **PASSED** |
| 11 | **TC11** | REST API | Service Health & Version | `GET /api/status` | HTTP 200 OK, JSON content-type, payload `{ ok: true, status: "online" }` | **PASSED** |
| 12 | **TC12** | REST API | Sesi Daring Google Meet | `GET /api/meet/aktif` | HTTP 200 OK, payload `{ ok: true, data: [...] }` berupa array data meet | **PASSED** |
| 13 | **TC13** | REST API | Data Leaderboard Kelas | `GET /api/leaderboard/1` | HTTP 200 OK, payload `{ ok: true, kelas_id: 1, data: [...] }` berupa array siswa | **PASSED** |
| 14 | **TC14** | REST API | Koleksi E-Book Perpustakaan | `GET /api/perpustakaan` | HTTP 200 OK, payload `{ ok: true, data: [...] }` berupa array koleksi e-book | **PASSED** |
| 15 | **TC15** | REST API | Jadwal Pelajaran Mingguan | `GET /api/jadwal/1` | HTTP 200 OK, payload `{ ok: true, kelas_id: 1, data: [...] }` berupa array jadwal | **PASSED** |

---

### B. Tabel Matriks 5 Test Cases Sengaja Gagal (Failed / Defect Simulation)

Dalam pengujian otomatis (Automation Testing), skenario kegagalan bertujuan membuktikan bahwa kerangka pengujian (Cypress) memiliki asersi yang tajam dalam mendeteksi ketidaksesuaian antarmuka, pelanggaran hak akses (security boundary), dan integritas data backend.

| No | Kode TC | Tipe Uji | Modul / Skenario | Ekspektasi Pengujian (Diharapkan Penguji) | Realitas Sistem & Alasan Kegagalan di Cypress | Status |
|---|---|---|---|---|---|:---:|
| 16 | **TC16** | UI / E2E | Validasi Form Kosong | Mengharapkan muncul teks: `"Password wajib diisi minimal 8 karakter dan mengandung simbol unik"` | **AssertionError (Timeout):** Form login menggunakan validasi native HTML5 / pesan umum, sehingga teks spesifik tersebut tidak ditemukan pada DOM. | **FAILED** |
| 17 | **TC17** | UI / E2E | Celah Akses Siswa ke Panel Admin | Mengharapkan siswa dapat melihat teks `"Kelola Data Seluruh Pengguna Sekolah"` di `/admin/pengguna` | **AssertionError:** Sistem LMS memiliki proteksi role guard yang kuat sehingga siswa menerima respons 403 / dialihkan, elemen admin tidak pernah dirender. | **FAILED** |
| 18 | **TC18** | UI / E2E | Integritas Data Leaderboard | Mengharapkan nama siswa fiktif `"Siswa Fiktif Tidak Nyata"` muncul di halaman ranking | **AssertionError (Timeout):** Teks nama fiktif tidak ditemukan dalam basis data atau DOM tabel peringkat. | **FAILED** |
| 19 | **TC19** | REST API | Request Rute Non-Eksis | Mengharapkan request `GET /api/data-rahasia-sekolah` mengembalikan status `200 OK` | **AssertionError:** Backend mengembalikan status `404 Not Found` karena endpoint tersebut memang tidak didaftarkan. | **FAILED** |
| 20 | **TC20** | REST API | Verifikasi Versi Rilis Backend | Mengharapkan nilai `response.body.version` bernilai `'2.5.0'` pada `GET /api/status` | **AssertionError:** Backend saat ini berjalan pada versi rilis `'1.0.0'`, sehingga perbandingan nilai menghasilkan ketidakcocokan. | **FAILED** |

---

### Cara Menjalankan di Cypress Test Runner

Jalankan perintah berikut pada terminal:
```bash
npx cypress open
```

1. Pilih menu **E2E Testing**.
2. Pilih browser **Chrome** lalu klik **Start E2E Testing in Chrome**.
3. Di panel Specs, klik file **`lms_full_suite.cy.js`**.
4. Cypress akan menjalankan ke-20 pengujian dan memberikan laporan:
   - **Passed: 15** (Warna Hijau)
   - **Failed: 5** (Warna Merah)
