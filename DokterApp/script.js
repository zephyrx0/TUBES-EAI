document.addEventListener('DOMContentLoaded', async function() {
    const dokterListElement = document.getElementById('dokterList');
    
    // Ambil data dokter dari file JSON
    const response = await fetch('dokter.dokter.json');
    const data = await response.json();
    
    // Loop melalui setiap data dokter dan tambahkan ke dalam elemen HTML
    data.forEach(dokter => {
        const dokterCard = `
            <div class="dokter-card">
                <img src="${dokter.foto}" alt="${dokter.namaDokter}'s Photo">
                <div class="dokter-info">
                    <h2>${dokter.namaDokter}</h2>
                    <p><strong>Poli:</strong> ${dokter.poli}</p>
                    <p>${dokter.deskripsi}</p>
                </div>
            </div>
        `;
        dokterListElement.insertAdjacentHTML('beforeend', dokterCard);
    });
});
