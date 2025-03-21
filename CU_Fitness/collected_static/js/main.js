// Function to fetch data from an API with error handling
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Fetch error:", error);
        return { suggestions: [] };  // Return empty data to prevent crashes
    }
}

// Get Workout Suggestions
async function getWorkoutSuggestions() {
    const workoutPlanId = document.getElementById('workout-plan').value;
    const data = await fetchData(`/api/workoutplans/${workoutPlanId}/ai_suggestion/`);
    displayWorkoutSuggestions(data.suggestions);
}

function displayWorkoutSuggestions(suggestions) {
    const workoutList = document.getElementById('workout-list');
    workoutList.innerHTML = '';
    if (suggestions.length === 0) {
        workoutList.innerHTML = '<li>No suggestions available.</li>';
    } else {
        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = `${suggestion.name} - ${suggestion.reps} reps, ${suggestion.duration} mins`;
            workoutList.appendChild(li);
        });
    }
}

// Get Nutrition Suggestions
async function getNutritionSuggestions() {
    const nutritionPlanId = document.getElementById('nutrition-plan').value;
    const data = await fetchData(`/api/nutritionplans/${nutritionPlanId}/ai_suggestion/`);
    displayNutritionSuggestions(data.suggestions);
}

function displayNutritionSuggestions(suggestions) {
    const nutritionList = document.getElementById('nutrition-list');
    nutritionList.innerHTML = '';
    if (suggestions.length === 0) {
        nutritionList.innerHTML = '<li>No suggestions available.</li>';
    } else {
        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = `${suggestion.meal} - Calories: ${suggestion.calories}, Protein: ${suggestion.protein}g`;
            nutritionList.appendChild(li);
        });
    }
}

// Get Progress Tracker Data
async function getProgressTracker() {
    const userId = document.getElementById('user-id').value;
    if (!userId) {
        alert("Please enter a user ID.");
        return;
    }
    const data = await fetchData(`/api/progresstracker/${userId}/progress/`);
    displayProgress(data);
}

function displayProgress(data) {
    const progressDataDiv = document.getElementById('progress-data');
    if (data.error) {
        progressDataDiv.textContent = 'No progress data found';
    } else {
        progressDataDiv.innerHTML = `
            <p>Weight: ${data.weight} kg</p>
            <p>Body Fat Percentage: ${data.body_fat_percentage}%</p>
            <p>Muscle Mass: ${data.muscle_mass} kg</p>
        `;
    }
}

// Handle Chatbot
document.getElementById('send-message').addEventListener('click', async () => {
    const userMessage = document.getElementById('user-message').value;
    if (!userMessage.trim()) {
        alert("Please enter a message.");
        return;
    }

    const response = await fetch('/api/ai_chatbot/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();
    displayChatbotReply(data.reply);
});

function displayChatbotReply(reply) {
    const chatbox = document.getElementById('chatbox');
    const message = document.createElement('p');
    message.textContent = `AI: ${reply}`;
    chatbox.appendChild(message);
    document.getElementById('user-message').value = '';  // Clear input
}
