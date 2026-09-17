import streamlit as st
from supabase import create_client, Client
from datetime import datetime

SUPABASE_URL = "https://dgtsaqfwluqpjvohhxar.supabase.co"
SUPABASE_KEY = "sb_publishable_AKg2-10-p2l06c6-2Q2Szg_ECnSWafa"
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Gagal inisialisasi Supabase: {e}")

def save_data(nama, alamat, nik, no_hp, skor, kategori):
    tanggal = datetime.now().isoformat()
    data = {
        "nama": nama,
        "alamat": alamat,
        "nik": nik,
        "no_hp": no_hp,
        "skor": skor,
        "kategori": kategori,
        "tanggal": tanggal
    }

    supabase.table("hasil_skrining").insert(data).execute()

st.set_page_config(page_title="SIGAP-BNNP-DIY", layout="centered")

url_logo = "https://upload.wikimedia.org/wikipedia/commons/c/cf/Logo_BNN.png"

st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: flex-start; gap: 20px;">
        <img src="{url_logo}" width="85" style="margin-top: 15px;">
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <h1 style="margin: 0; color: #1E3A8A; font-size: 36px; line-height: 1.0;">SIGAP-BNNP-DIY</h1>
            <p style="margin: 2px 0 0 0; font-size: 16px; color: #6B7280; font-weight: bold; line-height: 1.1;">
                Sistem Integrasi Skrining & Analisis Penggunaan Narkotika - BNNP DIY
            </p>
            <p style="margin: 0; font-size: 14px; color: #1E3A8A; font-style: italic; line-height: 1.1;">
                Klinik Seger Waras - BNNP D.I.Yogyakarta  (0274) 385378
            </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.subheader("Data Identitas")
col1, col2 = st.columns(2)
with col1:
    nama = st.text_input("Nama Lengkap *")
    nik = st.text_input("NIK (16 Digit) *")
with col2:
    no_hp = st.text_input("Nomor HP / WhatsApp *")
    alamat = st.text_area("Alamat Lengkap *", height=68)

st.divider()

total_score = 0

st.subheader("Riwayat Penggunaan Zat")
st.info("Pernahkah anda menggunakan zat berikut (di luar alasan medis)?")

list_zat = [
    "Tembakau", "Minuman Beralkohol", "Kanabis (Ganja)", "Kokain",
    "Stimulan (Shabu/Ekstasi)", "Inhalansia (Lem/Tiner)", "Sedativa (Obat Tidur)", "Halusinogens"
]

answers_b1 = []

cols_riwayat = st.columns(4)
for i, zat in enumerate(list_zat):
    with cols_riwayat[i % 4]:
        ans = st.radio(f"{zat}?", ("Ya", "Tidak"), index=1, key=f"b1_{i}")
        answers_b1.append(ans)
        if ans == "Ya":
            total_score += 1

st.divider()

st.subheader("Frekuensi Penggunaan (3 Bulan Terakhir)")

freq_map = {
    "Tidak Pernah": 0,
    "1-2x": 2,
    "Tiap Bulan": 3,
    "Tiap Minggu": 4,
    "Hampir Selalu": 6
}

ada_zat_aktif = False
for i, zat in enumerate(list_zat):
    if answers_b1[i] == "Ya":
        ada_zat_aktif = True
        freq_ans = st.selectbox(f"Seberapa sering menggunakan {zat}?", list(freq_map.keys()), key=f"b2_{i}")
        total_score += freq_map[freq_ans]

if not ada_zat_aktif:
    st.write("*(Pilih 'Ya' pada daftar di atas untuk mengisi frekuensi)*")

st.divider()

st.subheader("Dampak dan Masalah")

questions_b3 = [
    "Berdampak pada kesehatan, sosial, hukum, atau keuangan?",
    "Merasa sakit jika tidak menggunakan zat tersebut?",
    "Orang terdekat mengeluhkan perubahan sifat anda?",
    "Membawa/menyimpan zat di tempat berisiko tinggi?",
    "Pernah terjerat pidana masalah narkotika?",
    "Uang habis untuk zat dibanding kebutuhan pokok?"
]

for i, q in enumerate(questions_b3):
    ans_b3 = st.radio(f"{i+1}. {q}", ("Ya", "Tidak"), index=1, key=f"b3_{i}")
    if ans_b3 == "Ya":
        total_score += 1

st.divider()
if st.button("Analisis Hasil Skrining", use_container_width=True):
    if not (nama and nik and no_hp and alamat):
        st.error("⚠️ Data Belum Lengkap! Mohon lengkapi semua formulir identitas.")
    else:
        if total_score <= 3:
            kat, msg, icon_func = "Risiko Ringan", "Hasil skrining menunjukkan adanya risiko ringan terkait penggunaan zat. Disarankan untuk mendapatkan edukasi, pemantauan, dan intervensi awal guna mencegah peningkatan risiko penggunaan zat. Sehatmu Prioritas Kami. Periksa Tanpa Ragu, Pulih Tanpa Stigma di Klinik Seger Waras BNNP DIY", st.success
        elif 4 <= total_score <= 26:
            kat, msg, icon_func = "Risiko Sedang", "Hasil skrining menunjukkan adanya risiko sedang terkait penggunaan zat. Disarankan untuk mendapatkan asesmen lebih lanjut dan intervensi rehabilitasi sesuai kebutuhan guna mendukung perubahan perilaku dan mencegah risiko penggunaan zat berlanjut. Menjaga kesehatan adalah bentuk terbaik mencintai diri sendiri. Jangan biarkan rasa takut menghalangi langkahmu. Mari berkonsultasi secara aman dan nyaman bersama tim medis profesional Klinik Seger Waras BNNP DIY", st.warning
        else:
            kat, msg, icon_func = "Risiko Berat", "Hasil skrining menunjukkan adanya risiko berat terkait penggunaan zat. Disarankan untuk mendapatkan asesmen komprehensif dan penanganan rehabilitasi yang lebih intensif sesuai kebutuhan, termasuk evaluasi medis dan psikososial. Langkah awal menuju pulih dimulai dari keberanian untuk memeriksakan diri. Privat, profesional, dan ramah—Klinik Seger Waras BNNP DIY siap mendampingi Anda", st.error

        st.subheader(f"Hasil Analisis: {nama}")
        icon_func(f"**Total Skor: {total_score}**\n\nKategori: **{kat}**\n\n{msg}")

        try:
            save_data(nama, alamat, nik, no_hp, total_score, kat)
            st.info("✅ Data hasil skrining telah berhasil disimpan ke Supabase.")
        except Exception as e:
            st.error(f"Gagal menyimpan ke database: {e}")
