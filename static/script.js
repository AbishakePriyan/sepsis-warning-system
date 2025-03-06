// Navigation: (if additional functionality is desired)
document.addEventListener("DOMContentLoaded", function() {
  // Optionally add smooth scrolling if needed
  // Smooth scrolling can also be achieved with CSS: html { scroll-behavior: smooth; }
  
  // Handle Prediction Form Submission
  const predictForm = document.getElementById("predict-form");
  if (predictForm) {
    predictForm.addEventListener("submit", async function(event) {
      event.preventDefault();
      const formData = new FormData(predictForm);
      let data = {};
      formData.forEach((value, key) => { data[key] = value; });

      try {
        const response = await fetch("/api/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        const result = await response.json();
        const resultDiv = document.getElementById("prediction-result");
        if (result.sepsis_risk !== undefined) {
          resultDiv.textContent = `Prediction: ${result.sepsis_risk === 1 ? "High Risk of Sepsis" : "Low Risk of Sepsis"}`;
        } else {
          resultDiv.textContent = `Error: ${result.error}`;
        }
        resultDiv.style.display = "block";
      } catch (error) {
        console.error("Error connecting to API:", error);
      }
    });
  }

  // Handle Feedback Form Submission
  const feedbackForm = document.getElementById("feedback-form");
  if (feedbackForm) {
    feedbackForm.addEventListener("submit", async function(event) {
      event.preventDefault();
      const formData = new FormData(feedbackForm);
      let data = {};
      formData.forEach((value, key) => { data[key] = value; });

      try {
        const response = await fetch("/api/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        const result = await response.json();
        const resultDiv = document.getElementById("feedback-result");
        resultDiv.textContent = result.message ? result.message : "Submission error";
        resultDiv.style.display = "block";
        feedbackForm.reset();
      } catch (error) {
        console.error("Feedback submission error:", error);
      }
    });
  }
});
