function startVoiceInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Voice input not supported in your browser.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function (event) {
        document.getElementById("ingredients").value = event.results[0][0].transcript;
    };
}

async function generateRecipe() {
    const ingredients = document.getElementById("ingredients").value;
    const healthMode = document.getElementById("healthMode").value;
    const mode = document.getElementById("mode").value;

    if (!ingredients.trim()) {
        alert("Please enter ingredients.");
        return;
    }

    document.getElementById("results").innerHTML = "<h2>🍳 Finding recipes for you...</h2>";

    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            ingredients,
            healthMode,
            mode
        })
    });

    const data = await response.json();
    let html = "";

    if (!data.length) {
        html = "<h2>No recipes found. Try other ingredients 🍲</h2>";
    } else {
        data.forEach(recipe => {
            html += `
                <div class="card">
                    <img src="${recipe.image}" alt="${recipe.name}">
                    <h2>${recipe.name}</h2>
                    <p><strong>${recipe.badge}</strong></p>
                    <p>${recipe.instructions}</p>
                    <p>🔥 Calories: ${recipe.calories}</p>
                    <p>💪 Protein: ${recipe.protein}</p>
                    <p>✨ Match: ${recipe.match_percent}%</p>
                    <p>🧾 Missing: ${recipe.missing.length ? recipe.missing.join(', ') : 'None'}</p>
                    ${recipe.warning.length ? `<p class="warning">⚠ Avoid: ${recipe.warning.join(', ')}</p>` : ''}
                </div>
            `;
        });
    }

    document.getElementById("results").innerHTML = html;
}