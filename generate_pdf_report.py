import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# -------------------------------------------------------------------------
# NUMBERED CANVAS FOR HEADER & FOOTER WITH TOTAL PAGE COUNT
# -------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # Suppress headers/footers on cover page
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header
        self.drawString(54, 804, "Laporan Pengujian Otomatis LMS SMAN 10 Garut — Cypress Automation Suite")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 796, 541, 796)

        # Running Footer
        self.line(54, 46, 541, 46)
        self.drawString(54, 34, "Mata Kuliah: Pengujian Perangkat Lunak • SMAN 10 Garut")
        page_str = f"Halaman {self._pageNumber} dari {total_pages}"
        self.drawRightString(541, 34, page_str)

        self.restoreState()

# -------------------------------------------------------------------------
# MAIN PDF GENERATOR
# -------------------------------------------------------------------------
def build_pdf(filename="Laporan_Automation_Testing_LMS_SMAN_10_Garut.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom typography colors
    c_primary = colors.HexColor("#0f172a") # Slate 900
    c_blue    = colors.HexColor("#1d4ed8") # Blue 700
    c_green   = colors.HexColor("#059669") # Emerald 600
    c_red     = colors.HexColor("#b91c1c") # Red 700
    c_slate   = colors.HexColor("#475569") # Slate 600

    title_cover = ParagraphStyle('TitleCover', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=23, leading=27, textColor=c_primary, alignment=1)
    sub_cover   = ParagraphStyle('SubCover', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=c_blue, alignment=1)
    badge_cover = ParagraphStyle('BadgeCover', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor("#1e3a8a"), alignment=1)
    
    h1 = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=c_primary, spaceAfter=6)
    h2 = ParagraphStyle('H2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_blue, spaceBefore=6, spaceAfter=4)
    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_slate)
    body_bold = ParagraphStyle('BodyBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=c_primary)
    
    table_head = ParagraphStyle('THead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=colors.white, alignment=1)
    table_cell = ParagraphStyle('TCell', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=8.5, textColor=c_primary)
    table_cell_bold = ParagraphStyle('TCellBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=8.5, textColor=c_primary)
    table_cell_pass = ParagraphStyle('TCellPass', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=8.5, textColor=c_green, alignment=1)
    table_cell_fail = ParagraphStyle('TCellFail', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=8.5, textColor=c_red, alignment=1)
    caption = ParagraphStyle('Caption', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=c_slate, alignment=1, spaceBefore=3)

    story = []

    # =========================================================================
    # HALAMAN 1: COVER
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("PROGRAM STUDI TEKNIK INFORMATIKA / SISTEM INFORMASI", badge_cover))
    story.append(Paragraph("MATA KULIAH: PENGUJIAN PERANGKAT LUNAK (SOFTWARE TESTING & QA)", ParagraphStyle('TopDept', parent=sub_cover, fontSize=9.5, leading=13, textColor=c_slate)))
    story.append(Spacer(1, 30))

    story.append(HRFlowable(width="100%", thickness=3, color=c_blue, spaceAfter=22, spaceBefore=4))
    story.append(Paragraph("LAPORAN PENGUJIAN OTOMATIS<br/>(AUTOMATION TESTING REPORT)", title_cover))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Pengujian Black-Box End-to-End (E2E) Antarmuka Web & REST API Backend Berbasis Cypress v16 pada Sistem Learning Management System (LMS) SMAN 10 Garut", sub_cover))
    story.append(Spacer(1, 18))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=26, spaceBefore=4))

    summary_data = [
        [Paragraph("<b>Status Pengujian:</b>", body), Paragraph("<font color='#059669'><b>15 PASSED</b></font> | <font color='#b91c1c'><b>5 FAILED</b></font> (Total 20 Kasus Uji)", body)],
        [Paragraph("<b>Framework Uji:</b>", body), Paragraph("Cypress v16.3.0 & Node.js v24 (Browser: Google Chrome)", body)],
        [Paragraph("<b>Metode Pengujian:</b>", body), Paragraph("Automated Black-Box Testing (UI E2E + REST API Integration)", body)],
        [Paragraph("<b>Durasi Eksekusi:</b>", body), Paragraph("00:53 Detik (Full Suite Run)", body)],
        [Paragraph("<b>Aplikasi Target:</b>", body), Paragraph("LMS SMAN 10 Garut (Localhost Laragon Server)", body)],
        [Paragraph("<b>Waktu Pelaksanaan:</b>", body), Paragraph("November 2026", body)],
    ]
    t_summary = Table(summary_data, colWidths=[140, 320])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_summary)

    story.append(Spacer(1, 35))
    meta_box = [
        [Paragraph("<b>Disusun Oleh:</b>", body_bold)],
        [Paragraph("Mahasiswa Penguji: <b>Yunus Fahreza / Tim Penguji SQA</b>", body)],
        [Paragraph("NIM / Program Studi: <b>Teknik Informatika — Praktikum Otomasi</b>", body)],
        [Paragraph("Dosen Pengampu: <b>Dosen Penguji Perangkat Lunak</b>", body)],
    ]
    t_meta = Table(meta_box, colWidths=[460])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bfdbfe")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_meta)

    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 2: BAB I - PENDAHULUAN & LINGKUNGAN PENGUJIAN
    # =========================================================================
    story.append(Paragraph("BAB I: PENDAHULUAN & LINGKUNGAN PENGUJIAN", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph("1.1 Latar Belakang Pengujian", h2))
    p1 = ("Pengujian perangkat lunak secara otomatis (*Automation Testing*) merupakan standar industri krusial untuk "
          "menjamin kualitas, stabilitas, dan keandalan sistem aplikasi. Pada sistem <b>LMS SMAN 10 Garut</b>, pengujian "
          "otomatis menggunakan kerangka kerja <b>Cypress</b> diterapkan untuk memverifikasi fungsionalitas antarmuka "
          "pengguna (*User Interface*) multi-peran, integritas data penilaian dan gamifikasi, serta ketahanan titik akhir "
          "antarmuka pemrograman aplikasi (*REST API Endpoints*).")
    story.append(Paragraph(p1, body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.2 Objek Sistem yang Diuji", h2))
    p2 = ("Objek pengujian adalah platform LMS SMAN 10 Garut yang mencakup 5 modul inti: "
          "(1) Sistem Autentikasi & Guard Hak Akses berbasis peran Admin, Guru, dan Siswa; "
          "(2) Modul Tatap Muka Daring terintegrasi Google Meet; "
          "(3) Modul Gamifikasi Prestasi & Papan Peringkat (Leaderboard); "
          "(4) Modul Perpustakaan Digital & Repositori Modul; serta "
          "(5) Layanan REST API publik untuk integrasi data mobile/eksternal.")
    story.append(Paragraph(p2, body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.3 Spesifikasi Lingkungan Pengujian (Test Environment)", h2))
    env_data = [
        [Paragraph("Komponen", table_head), Paragraph("Spesifikasi Lingkungan", table_head), Paragraph("Keterangan", table_head)],
        [Paragraph("Sistem Operasi", table_cell_bold), Paragraph("Microsoft Windows 10/11 (64-bit)", table_cell), Paragraph("Host Environment", table_cell)],
        [Paragraph("Web Server & DB", table_cell_bold), Paragraph("Apache 2.4.54 / MariaDB (MySQL 5.7) via Laragon", table_cell), Paragraph("Localhost Environment", table_cell)],
        [Paragraph("Backend Platform", table_cell_bold), Paragraph("PHP 8.1 / 8.2 (MVC Native Architecture)", table_cell), Paragraph("Production Framework", table_cell)],
        [Paragraph("Automation Framework", table_cell_bold), Paragraph("Cypress v16.3.0 & Node.js v24.x", table_cell), Paragraph("E2E & API Test Engine", table_cell)],
        [Paragraph("Browser Uji", table_cell_bold), Paragraph("Google Chrome v120 (Headless / Interactive Mode)", table_cell), Paragraph("Target Client Browser", table_cell)],
        [Paragraph("URL Basis Aplikasi", table_cell_bold), Paragraph("http://localhost/ptvantagesejahtera-main/public", table_cell), Paragraph("Base URL Config", table_cell)],
    ]
    t_env = Table(env_data, colWidths=[120, 230, 137])
    t_env.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_env)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.4 Metodologi Pengujian (Testing Methodology)", h2))
    p3 = ("Pengujian diklasifikasikan ke dalam <b>Automated Black-Box Testing</b> dengan dua pendekatan utama:<br/>"
          "• <b>Positive Testing (15 Kasus Uji):</b> Memverifikasi bahwa seluruh alur kerja sistem berjalan sesuai spesifikasi kebutuhan (SRS/PRD).<br/>"
          "• <b>Negative Testing & Defect Simulation (5 Kasus Uji):</b> Memverifikasi ketajaman asersi Cypress dalam mendeteksi anomali input, pelanggaran proteksi hak akses, dan endpoint tidak ditemukan.")
    story.append(Paragraph(p3, body))

    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 3: BAB II - MATRIKS SEMUA KASUS UJI (TC01 - TC20 COMPACT)
    # =========================================================================
    story.append(Paragraph("BAB II: MATRIKS & SKENARIO PENGUJIAN (TEST MATRIX)", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("2.1 Matriks 15 Kasus Uji Berhasil (Passed Test Cases)", h2))
    story.append(Paragraph("Seluruh 15 kasus uji di bawah ini telah dieksekusi oleh Cypress dan menghasilkan status <b>PASSED (100% Lolos)</b>.", body))
    story.append(Spacer(1, 3))

    tc_passed_data = [
        [Paragraph("ID", table_head), Paragraph("Tipe", table_head), Paragraph("Modul / Skenario", table_head), Paragraph("Input / Rute", table_head), Paragraph("Hasil yang Diharapkan", table_head), Paragraph("Status", table_head)],
        [Paragraph("TC01", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Login Siswa Valid", table_cell), Paragraph("siswa.raesa / siswa12345", table_cell), Paragraph("Redirect /siswa, nama Raesa Gista tampil", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC02", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Login Guru Valid", table_cell), Paragraph("guru.siti / guru12345", table_cell), Paragraph("Redirect /guru, nama Siti Rahmawati tampil", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC03", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Login Admin Valid", table_cell), Paragraph("admin / admin12345", table_cell), Paragraph("Redirect /admin, nama Administrator tampil", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC04", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Validasi Password Salah", table_cell), Paragraph("siswa.raesa / salah123", table_cell), Paragraph("Tetap di /login, alert error tampil", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC05", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Validasi Akun Tak Terdaftar", table_cell), Paragraph("user.fiktif / bebas123", table_cell), Paragraph("Tetap di /login, alert error tampil", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC06", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Proteksi Hak Akses Guest", table_cell), Paragraph("Akses URL /siswa langsung", table_cell), Paragraph("Ditolak, otomatis redirect ke /login", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC07", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Integrasi Google Meet", table_cell), Paragraph("Dashboard Siswa", table_cell), Paragraph("Card Meet Live dan tombol gabung ada", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC08", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Leaderboard & Ranking", table_cell), Paragraph("URL /siswa/pencapaian", table_cell), Paragraph("Papan peringkat & Raesa Rank 1 tampil", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC09", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Katalog E-Perpustakaan", table_cell), Paragraph("URL /perpustakaan", table_cell), Paragraph("Koleksi e-book & modul digital tampil", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC10", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Terminasi Sesi Logout", table_cell), Paragraph("Submit logout token CSRF", table_cell), Paragraph("Sesi terhapus, akses kembali tertolak", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC11", table_cell_bold), Paragraph("API", table_cell), Paragraph("Service Health Check", table_cell), Paragraph("GET /api/status", table_cell), Paragraph("HTTP 200 OK, JSON status online", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC12", table_cell_bold), Paragraph("API", table_cell), Paragraph("Daftar Sesi Google Meet", table_cell), Paragraph("GET /api/meet/aktif", table_cell), Paragraph("HTTP 200 OK, payload array data meet", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC13", table_cell_bold), Paragraph("API", table_cell), Paragraph("Leaderboard Siswa Kelas", table_cell), Paragraph("GET /api/leaderboard/1", table_cell), Paragraph("HTTP 200 OK, payload array ranking", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC14", table_cell_bold), Paragraph("API", table_cell), Paragraph("Katalog Buku Digital", table_cell), Paragraph("GET /api/perpustakaan", table_cell), Paragraph("HTTP 200 OK, payload array buku", table_cell), Paragraph("PASSED", table_cell_pass)],
        [Paragraph("TC15", table_cell_bold), Paragraph("API", table_cell), Paragraph("Jadwal Pelajaran Kelas", table_cell), Paragraph("GET /api/jadwal/1", table_cell), Paragraph("HTTP 200 OK, payload array jadwal", table_cell), Paragraph("PASSED", table_cell_pass)],
    ]
    t_passed = Table(tc_passed_data, colWidths=[26, 23, 115, 110, 163, 50])
    t_passed.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(t_passed)

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.2 Matriks 5 Kasus Uji Negatif & Simulasi Defect (Failed Test Cases)", h2))
    story.append(Paragraph("Kasus uji di bawah ini sengaja dirancang gagal untuk membuktikan kepekaan dan validitas asersi Cypress.", body))
    story.append(Spacer(1, 3))

    tc_failed_data = [
        [Paragraph("ID", table_head), Paragraph("Tipe", table_head), Paragraph("Skenario Defect", table_head), Paragraph("Ekspektasi Asersi Uji", table_head), Paragraph("Realitas Sistem & Alasan Gagal", table_head), Paragraph("Status", table_head)],
        [Paragraph("TC16", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Validasi Form Login Kosong", table_cell), Paragraph("Cari teks 'Password minimal 8 kar & simbol'", table_cell), Paragraph("Form menggunakan validasi umum, teks spesifik tidak ada (Timeout 4s)", table_cell), Paragraph("FAILED", table_cell_fail)],
        [Paragraph("TC17", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Celah Hak Akses Siswa", table_cell), Paragraph("Siswa dapat melihat judul panel admin", table_cell), Paragraph("Role guard sistem menolak siswa (403/redirect), elemen tidak pernah muncul", table_cell), Paragraph("FAILED", table_cell_fail)],
        [Paragraph("TC18", table_cell_bold), Paragraph("UI", table_cell), Paragraph("Integritas Data Leaderboard", table_cell), Paragraph("Cari nama siswa 'Siswa Fiktif Tidak Nyata'", table_cell), Paragraph("Data fiktif tidak ada di database, asersi gagal setelah 4000ms", table_cell), Paragraph("FAILED", table_cell_fail)],
        [Paragraph("TC19", table_cell_bold), Paragraph("API", table_cell), Paragraph("Request Rute Non-Eksis", table_cell), Paragraph("GET /api/data-rahasia -> Status 200", table_cell), Paragraph("Endpoint tidak terdaftar, backend merespons 404 (expected 404 to equal 200)", table_cell), Paragraph("FAILED", table_cell_fail)],
        [Paragraph("TC20", table_cell_bold), Paragraph("API", table_cell), Paragraph("Verifikasi Versi Rilis API", table_cell), Paragraph("Respons version bernilai '2.5.0'", table_cell), Paragraph("Backend saat ini berjalan pada v1.0.0 (expected '1.0.0' to equal '2.5.0')", table_cell), Paragraph("FAILED", table_cell_fail)],
    ]
    t_failed = Table(tc_failed_data, colWidths=[26, 23, 115, 110, 163, 50])
    t_failed.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#7f1d1d")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#fca5a5")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#fef2f2")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(t_failed)

    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 4: BAB III - BUKTI CYPRESS RUNNER (SCREENSHOT 1)
    # =========================================================================
    story.append(Paragraph("BAB III: BUKTI EKSEKUSI PENGUJIAN (TEST EXECUTION EVIDENCE)", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("3.1 Bukti Eksekusi Master Test Suite Cypress Runner", h2))
    story.append(Paragraph("Gambar 3.1 di bawah ini memperlihatkan antarmuka Cypress Test Runner saat mengeksekusi file master <b>lms_full_suite.cy.js</b>. Seluruh hierarki pengujian terbukti dijalankan secara simultan dan menghasilkan rekapitulasi <b>15 Passed</b> serta <b>5 Failed</b> secara transparan dalam durasi 53 detik.", body))
    story.append(Spacer(1, 6))

    img_runner = "docs/screenshots/cypress_full_run.png"
    if os.path.exists(img_runner):
        story.append(Image(img_runner, width=470, height=490))
        story.append(Paragraph("Gambar 3.1: Tangkapan Layar Cypress Test Runner (20 Kasus Uji: 15 Passed & 5 Failed)", caption))

    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 5: BUKTI UI TESTING & REST API TESTING (SCREENSHOTS 2 & 3)
    # =========================================================================
    story.append(Paragraph("3.2 Bukti Verifikasi DOM Antarmuka Web (UI Automation)", h2))
    story.append(Paragraph("Pengujian UI memvalidasi keberhasilan otentikasi siswa, kehadiran sesi Google Meet daring yang berstatus <i>LIVE SEKARANG</i>, serta konsistensi data leaderboard kelas.", body))
    story.append(Spacer(1, 4))

    img_ui = "docs/screenshots/lms_web_dashboard.png"
    if os.path.exists(img_ui):
        story.append(Image(img_ui, width=470, height=255))
        story.append(Paragraph("Gambar 3.2: Verifikasi DOM Halaman Dashboard Siswa & Integrasi Google Meet", caption))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.3 Bukti Otomasi & Inspeksi Jaringan REST API", h2))
    story.append(Paragraph("Pengujian API menggunakan <code>cy.request()</code> menguji ketersediaan endpoint backend secara langsung tanpa melalui rendering browser. Gambar 3.3 menunjukkan hasil asersi status 200 pada rute resmi serta asersi kegagalan status 404 pada rute fiktif.", body))
    story.append(Spacer(1, 4))

    img_api = "docs/screenshots/cypress_api_tests.png"
    if os.path.exists(img_api):
        story.append(Image(img_api, width=470, height=245))
        story.append(Paragraph("Gambar 3.3: Inspeksi Jaringan Cypress REST API Automation (Validasi Status & Payload JSON)", caption))

    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 6: BAB IV - ANALISIS HASIL & KESIMPULAN
    # =========================================================================
    story.append(Paragraph("BAB IV: ANALISIS HASIL PENGUJIAN & KESIMPULAN", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph("4.1 Evaluasi Kinerja Pengujian", h2))
    p_eval = ("Berdasarkan eksekusi 20 kasus uji selama 53 detik, sistem LMS SMAN 10 Garut terbukti stabil dan memiliki "
              "kecepatan respons yang optimal. Seluruh 15 kasus uji fungsional utama (TC01 s.d. TC15) berhasil dilalui "
              "tanpa adanya kesalahan teknis (*zero fatal errors*). Mekanisme session cookie dan proteksi CSRF token "
              "bekerja secara presisi pada setiap form pengiriman data.")
    story.append(Paragraph(p_eval, body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.2 Analisis Simulasi Kegagalan (Defect Detection & Boundary Testing)", h2))
    p_defect = ("Kelima kasus uji yang gagal (TC16 s.d. TC20) memberikan wawasan teknis yang bernilai tinggi bagi tim pengembang:<br/>"
                "1. <b>Proteksi Hak Akses (TC17):</b> Kegagalan TC17 membuktikan bahwa sistem keamanan LMS bekerja dengan sempurna karena peran Siswa ditolak mentah-mentah saat mencoba mengintip halaman pengelolaan Admin.<br/>"
                "2. <b>Keandalan Endpoint REST API (TC19):</b> Kegagalan TC19 memvalidasi bahwa web server tidak mengekspos endpoint fiktif sembarangan dan secara benar mengembalikan HTTP 404 Not Found.<br/>"
                "3. <b>Konsistensi Kontrak Data (TC20):</b> Cypress mampu mendeteksi ketidaksesuaian kecil antara spesifikasi versi rilis yang diharapkan dengan respons aktual backend.")
    story.append(Paragraph(p_defect, body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.3 Kesimpulan Akhir", h2))
    p_concl = ("Pengujian otomatis (*Automation Testing*) dengan kerangka kerja Cypress telah berhasil diterapkan secara komprehensif "
               "pada LMS SMAN 10 Garut. Sistem terbukti memenuhi syarat kelayakan fungsional (*Functional Readiness*), memiliki "
               "keamanan batas peran (*Role Guard Security*) yang kokoh, serta memiliki antarmuka REST API yang siap diintegrasikan. "
               "Laporan ini merekomendasikan sistem LMS untuk melangkah ke tahap pengujian beban (*Performance/Load Testing*) lanjutan.")
    story.append(Paragraph(p_concl, body))

    story.append(Spacer(1, 25))

    # Signature box
    sig_data = [
        [Paragraph("", body), Paragraph("Garut, 23 November 2026", ParagraphStyle('DateSig', parent=body, alignment=1))],
        [Paragraph("Mengetahui,<br/><b>Dosen Pengampu Mata Kuliah</b>", ParagraphStyle('SigTitle', parent=body, alignment=1)),
         Paragraph("Pelaksana Pengujian,<br/><b>Mahasiswa / Lead Tester SQA</b>", ParagraphStyle('SigTitle2', parent=body, alignment=1))],
        [Spacer(1, 40), Spacer(1, 40)],
        [Paragraph("( ............................................................ )", ParagraphStyle('Dots1', parent=body, alignment=1)),
         Paragraph("( <b>Yunus Fahreza / Tim Penguji</b> )", ParagraphStyle('Dots2', parent=body, alignment=1))],
    ]
    t_sig = Table(sig_data, colWidths=[240, 247])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_sig)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Optimized 6-page PDF Report generated successfully: {filename}")

if __name__ == "__main__":
    build_pdf()
