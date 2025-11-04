document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch and update cattle count
    function updateCattleCount() {
        fetch("/cattle/count") // Use the API endpoint
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const countElement = document.getElementById("cattle-count");
                if (countElement) {
                    countElement.textContent = data.total_count;
                }
            })
            .catch(error => {
                console.error("Error fetching cattle count:", error);
                const countElement = document.getElementById("cattle-count");
                if (countElement) {
                    countElement.textContent = "Erro"; // Indicate error
                }
            });
    }

    // Update count when the page loads
    updateCattleCount();

    // Optionally, update periodically (e.g., every 30 seconds)
    // setInterval(updateCattleCount, 30000);

    // Add event listeners for forms if they exist on the page
//    const addCattleForm = document.getElementById("add-cattle-form");
//    if (addCattleForm) {
//        addCattleForm.addEventListener("submit", handleAddCattle);
//    }
//
//    const addBirthForm = document.getElementById("add-birth-form");
//    if (addBirthForm) {
//        addBirthForm.addEventListener("submit", handleAddBirth);
//    }
});

// Placeholder functions for form handling (to be implemented fully later)
function handleAddCattle(event) {
    event.preventDefault();
    console.log("Add Cattle form submitted");
    // Add logic to collect form data and POST to /cattle/ endpoint
    alert("Funcionalidade de adicionar gado ainda não implementada completamente no frontend.");
}

function handleAddBirth(event) {
    event.preventDefault();
    console.log("Add Birth form submitted");
    // Add logic to collect form data and POST to /cattle/birth endpoint
    alert("Funcionalidade de adicionar nascimento ainda não implementada completamente no frontend.");
}

