document.addEventListener("DOMContentLoaded", () => {
  const cameras = document.querySelectorAll(".camera img");
  const solveButton = document.getElementById("solve-equation-btn");
  const answerInput = document.getElementById("equation-answer");

  const notificationArea = document.getElementById("notification-area");
  const notificationMessage = document.getElementById("notification-message");
  const nextChallengeBtn = document.getElementById("next-challenge-btn");


  // Solve equation event
  solveButton.addEventListener("click", async () => {
    const userAnswer = answerInput.value.trim();

    try {
      const response = await fetch("/check-answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: "camera_equation",
          answer: userAnswer,
        }),
      });

      const result = await response.json();
      showNotification(result.message);

      if (result.success) {
        // Show "Next Challenge" button and store the URL to the next challenge
        nextChallengeBtn.style.display = "block"; // Show the button
        nextChallengeBtn.onclick = () => {
          window.location.href = result.next_challenge_url; // Redirect to the next challenge
        };
      }
    } catch (error) {
      showNotification("Error checking your answer. Please try again.");
    }
  });

  // Show the notification next to Camera 4
  function showNotification(message) {
    notificationMessage.textContent = message;
    notificationArea.style.display = "block";

    // Hide the notification after 5 seconds
    setTimeout(() => {
      notificationArea.style.display = "none";
    }, 5000); // Hide after 5 seconds
  }
});
