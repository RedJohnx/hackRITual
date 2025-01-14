document.addEventListener("DOMContentLoaded", () => {
  const caesarForm = document.getElementById("caesar-cipher-form");
  const binaryForm = document.getElementById("binary-puzzle-form");
  const caesarResult = document.getElementById("caesar-result");
  const binaryResult = document.getElementById("binary-result");

  // Caesar Cipher Challenge
  caesarForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(caesarForm);
    const response = await fetch("/caesar-cipher", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    caesarResult.textContent = data.message;

    if (data.route) {
      caesarResult.style.color = "green";
    } else {
      caesarResult.style.color = "red";
    }
  });

  // Binary Decoding Challenge
  binaryForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(binaryForm);
    const response = await fetch("/binary-puzzle", {
      method: "POST",
      body: formData,
    });

    const result = await response.text();
    binaryResult.textContent = result;

    if (result.startsWith("Correct")) {
      binaryResult.style.color = "green";
    } else {
      binaryResult.style.color = "red";
    }
  });
});
