<?php

namespace App\Controllers;

use App\Core\Controller;
use App\Models\GoogleMeet;
use App\Models\Pencapaian;
use App\Models\Perpustakaan;
use App\Models\Jadwal;

final class ApiController extends Controller
{
    /**
     * Endpoint: GET /api/status
     */
    public function status(): void
    {
        $this->json([
            'ok'        => true,
            'app'       => 'LMS SMAN 10 Garut API',
            'status'    => 'online',
            'timestamp' => time(),
            'version'   => '1.0.0',
        ]);
    }

    /**
     * Endpoint: GET /api/meet/aktif
     */
    public function meetAktif(): void
    {
        $meetModel = new GoogleMeet();
        $daftar    = $meetModel->semuaUntukAdmin();

        $this->json([
            'ok'    => true,
            'total' => count($daftar),
            'data'  => $daftar,
        ]);
    }

    /**
     * Endpoint: GET /api/leaderboard/{id}
     */
    public function leaderboard(string $kelasId): void
    {
        $id          = $this->idWajib($kelasId);
        $pencapaian  = new Pencapaian();
        $leaderboard = $pencapaian->leaderboardKelas($id);

        $this->json([
            'ok'       => true,
            'kelas_id' => $id,
            'total'    => count($leaderboard),
            'data'     => $leaderboard,
        ]);
    }

    /**
     * Endpoint: GET /api/perpustakaan
     */
    public function perpustakaan(): void
    {
        $perpus = new Perpustakaan();
        $buku   = $perpus->daftar();

        $this->json([
            'ok'    => true,
            'total' => count($buku),
            'data'  => $buku,
        ]);
    }

    /**
     * Endpoint: GET /api/jadwal/{id}
     */
    public function jadwal(string $kelasId): void
    {
        $id     = $this->idWajib($kelasId);
        $jadwal = new Jadwal();
        $daftar = $jadwal->untukKelas($id);

        $this->json([
            'ok'       => true,
            'kelas_id' => $id,
            'total'    => count($daftar),
            'data'     => $daftar,
        ]);
    }
}
