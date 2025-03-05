document.addEventListener("DOMContentLoaded", function() {
    // Handle Navigation between Sections
    const navLinks = document.querySelectorAll(".nav-link");
    const sections = document.querySelectorAll(".section");
  
    navLinks.forEach(link => {
      link.addEventListener("click", function(e) {
        e.preventDefault();
        const targetId = this.getAttribute("href").substring(1);
        // Remove active class from all nav links and sections
        navLinks.forEach(link => link.classList.remove("active"));
        sections.forEach(section => section.classList.remove("active"));
  
        // Add active class to clicked nav link and corresponding section
        this.classList.add("active");
        document.getElementById(targetId).classList.add("active");
      });
    });
  
    // Handle Sepsis Prediction Form Submission
    const sepsisForm = document.getElementById("sepsisForm");
    sepsisForm.addEventListener("submit", async function(e) {
      e.preventDefault();
  
      const heartRate = parseFloat(document.getElementById("heartRate").value);
      const respRate = parseFloat(document.getElementById("respRate").value);
      const temperature = parseFloat(document.getElementById("temperature").value);
      const wbc = parseFloat(document.getElementById("wbc").value);
      const lactate = parseFloat(document.getElementById("lactate").value);
  
      const data = {
        HeartRate: heartRate,
        RespRate: respRate,
        Temp: temperature,
        WBC: wbc,
        Lactate: lactate
      };
  
      try {
        const response = await fetch("/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        const result = await response.json();
        const predictResultDiv = document.getElementById("predictResult");
        if (result.sepsis_risk !== undefined) {
          predictResultDiv.innerText = `Sepsis Risk: ${result.sepsis_risk}`;
        } else {
          predictResultDiv.innerText = `Error: ${result.error || "Unknown error"}`;
        }
      } catch (error) {
        console.error("Error connecting to API:", error);
        document.getElementById("predictResult").innerText = "Error connecting to the server.";
      }
    });
  
    // Handle Feedback Form Submission
    const feedbackForm = document.getElementById("feedbackForm");
    feedbackForm.addEventListener("submit", function(e) {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const feedbackText = document.getElementById("feedbackText").value;
      const feedbackResultDiv = document.getElementById("feedbackResult");
      
      // Simulate feedback submission success
      feedbackResultDiv.innerText = "Thank you for your feedback, " + name + "!";
      feedbackForm.reset();
      setTimeout(() => {
        feedbackResultDiv.innerText = "";
      }, 5000);
    });
  });
  