// script.js

async function generateExcuse() {
    const urgency = document.getElementById("urgency").value;
    const believability = document.getElementById("believability").value;
    const context = document.getElementById("context").value;
    const audience = document.getElementById("audience").value;
    const type = document.getElementById("type").value;
    const includeProof = document.getElementById("includeProof").checked;
  
    const response = await fetch("http://127.0.0.1:8000/generate_excuse", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            urgency,
            believability,
            context,
            audience,
            type,
            includeProof
        })
    });
  
    const data = await response.json();
    document.getElementById("excuseOutput").textContent = data.excuse;
  
    if (data.proof) {
        document.getElementById("proofSection").style.display = "block";
        document.getElementById("proofOutput").textContent = data.proof;
        document.getElementById("audioControls").style.display = "block";
    } else {
        document.getElementById("proofSection").style.display = "none";
    }
  }
  
  document.getElementById("generateBtn").addEventListener("click", generateExcuse);
  
const stars = document.querySelectorAll(".star");
let currentRating = 0;

stars.forEach((star) => {
  star.addEventListener("click", () => {
    currentRating = parseInt(star.getAttribute("data-value"));
    stars.forEach((s, i) => {
      s.classList.toggle("selected", i < currentRating);
    });

    // Send rating to backend
    sendRating(currentRating);
  });
});

async function sendRating(rating) {
    const excuse = document.getElementById("excuseOutput").textContent;
  
    if (!excuse || !rating) {
      console.warn("No excuse or rating to send.");
      return;
    }
  
    try {
      await fetch("http://127.0.0.1:8000/rate_excuse", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          excuse,
          rating,
        }),
      });
  
      storeRatingLocally(excuse, rating);
    } catch (error) {
      console.error("Error submitting rating:", error);
    }
  }
  document.addEventListener("DOMContentLoaded", function () {
  const believabilitySlider = document.getElementById("believability");
  const believabilityValue = document.getElementById("believabilityValue");

  believabilitySlider.addEventListener("input", function () {
    believabilityValue.textContent = `${this.value}%`;
  });
});

  function storeRatingLocally(excuse, rating) {
    const ratings = JSON.parse(localStorage.getItem("excuseRatings") || "{}");
    ratings[excuse] = rating;
    localStorage.setItem("excuseRatings", JSON.stringify(ratings));
    console.log("Rating stored in localStorage:", { excuse, rating });
  
    // Removed: displayRatingStars(rating); // No such function exists
  }
  
  
  function showTopRatedExcuse() {
    const ratings = JSON.parse(localStorage.getItem("excuseRatings") || "{}");
  
    const excuses = Object.entries(ratings); // [excuse, rating]
  
    if (excuses.length === 0) {
      alert("No rated excuses yet!");
      return;
    }
  
    // Sort by rating, descending
    const sorted = excuses.sort((a, b) => b[1] - a[1]);
  
    const leaderboard = document.getElementById("leaderboard");
    const leaderboardContent = document.getElementById("leaderboardContent");
    leaderboardContent.innerHTML = ""; // Clear existing
  
    sorted.slice(0, 5).forEach(([excuse, rating], index) => {
      const div = document.createElement("div");
      div.className = "leaderboard-entry";
      div.innerHTML = `
        <strong>#${index + 1}</strong><br>
        <em>${excuse}</em><br>
        ⭐ ${rating}/5
      `;
      leaderboardContent.appendChild(div);
    });
    
  
    leaderboard.style.display = "block"; // Show the leaderboard
  }
  
  
  document.getElementById("showTopRatedBtn").addEventListener("click", () => {
    const leaderboard = document.getElementById("leaderboard");
  
    if (leaderboard.style.display === "none" || leaderboard.style.display === "") {
      showTopRatedExcuse(); // This also sets display: block
    } else {
      leaderboard.style.display = "none";
    }
  });