document.getElementById("home-logo").addEventListener("click", function() {
  window.location.href = "index.html";
});

// Handle Prediction Form Submission
document.getElementById("predict-form").addEventListener("submit", async function(event) {
  event.preventDefault();

  const formData = new FormData(this);
  let data = {};
  formData.forEach((value, key) => { data[key] = value; });

  let response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
  });

  let result = await response.json();
  document.getElementById("prediction-result").textContent = 
      result.sepsis_risk ? "⚠️ High Risk of Sepsis!" : "✅ Low Risk of Sepsis";
});

// Handle Feedback Form Submission
document.getElementById("feedback-form").addEventListener("submit", async function(event) {
  event.preventDefault();

  const formData = new FormData(this);
  let data = {};
  formData.forEach((value, key) => { data[key] = value; });

  let response = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
  });

  let result = await response.json();
  document.getElementById("feedback-result").textContent = result.message;
});
