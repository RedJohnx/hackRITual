document.addEventListener("DOMContentLoaded", () => {
  const bookCipherForm = document.getElementById("book-cipher-form");
  const resultDiv = document.getElementById("cipher-result");

  bookCipherForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(bookCipherForm);
    const response = await fetch("/book-cipher", {
      method: "POST",
      body: formData,
    });

    const result = await response.text();
    resultDiv.textContent = result;

    if (response.status === 200) {
      resultDiv.style.color = "green";
    } else {
      resultDiv.style.color = "red";
    }
  });
});
document.addEventListener('DOMContentLoaded', () => {
    const vigenereForm = document.getElementById('vigenere-form');
    const vigenereResultDiv = document.getElementById('vigenere-result');

    vigenereForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(vigenereForm);
        const response = await fetch('/vigenere-cipher', {
            method: 'POST',
            body: formData
        });

        const result = await response.text();
        vigenereResultDiv.textContent = result;

        if (response.status === 200) {
            vigenereResultDiv.style.color = 'green';
        } else {
            vigenereResultDiv.style.color = 'red';
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const qrCodeContainer = document.getElementById('qr-code-container');

    // Fetch QR Code from the server
    async function loadQRCode() {
        const response = await fetch('/qr-code');
        const data = await response.json();

        // Display QR Code
        const img = document.createElement('img');
        img.src = `data:image/png;base64,${data.qr_code}`;
        img.alt = "QR Code";
        qrCodeContainer.innerHTML = "";
        qrCodeContainer.appendChild(img);
    }

    loadQRCode();
});
