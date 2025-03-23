// ✅ Utility function to retrieve CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ✅ Function to calculate BMI
function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);

    if (!weight || !height) {
        alert('Please enter both weight and height');
        return;
    }

    const bmi = weight / (height * height);
    document.getElementById('bmi-result').textContent = `Your BMI is: ${bmi.toFixed(2)}`;
}

// ✅ Fetch AI-generated workout recommendations
async function fetchWorkoutRecommendation() {
    try {
        const goal = document.getElementById('workout-goal').value;
        const response = await fetch(`/workout/recommend/?goal=${goal}`);

        if (!response.ok) throw new Error(`Workout API Error: ${response.status}`);

        const data = await response.json();
        document.getElementById('workout-recommendation').innerHTML = `
            <p><strong>Exercise:</strong> ${data.exercise || "Not Available"}</p>
            <p><strong>Sets:</strong> ${data.sets || "N/A"}</p>
            <p><strong>Reps:</strong> ${data.reps || "N/A"}</p>
            <p><strong>Intensity:</strong> ${data.intensity || "N/A"}</p>
        `;
    } catch (error) {
        console.error("Workout fetch error:", error);
        document.getElementById('workout-recommendation').innerHTML = "<p>⚠️ Unable to load workout recommendation.</p>";
    }
}

// ✅ Fetch AI-generated meal recommendations
async function fetchMealRecommendation() {
    try {
        const mealType = document.getElementById('meal-type').value;
        const response = await fetch(`/meal/recommend/?meal_type=${mealType}`);

        if (!response.ok) throw new Error(`Meal API Error: ${response.status}`);

        const data = await response.json();
        document.getElementById('meal-recommendation').innerHTML = `
            <p><strong>Meal:</strong> ${data.meal || "Not Available"}</p>
            <p><strong>Calories:</strong> ${data.calories || "N/A"} kcal</p>
            <p><strong>Protein:</strong> ${data.protein || "N/A"}g</p>
            <p><strong>Carbs:</strong> ${data.carbs || "N/A"}g</p>
            <p><strong>Fats:</strong> ${data.fats || "N/A"}g</p>
        `;
    } catch (error) {
        console.error("Meal fetch error:", error);
        document.getElementById('meal-recommendation').innerHTML = "<p>⚠️ Unable to load meal recommendation.</p>";
    }
}

// ✅ Fetch AI chatbot response with CSRF protection
async function fetchChatbotResponse() {
    const userMessage = document.getElementById('user-message').value.trim();
    if (!userMessage) {
        alert("Please enter a message.");
        return;
    }

    try {
        const csrftoken = getCookie('csrftoken');

        const response = await fetch('/api/ai_chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) throw new Error(`Chatbot API Error: ${response.status}`);

        const data = await response.json();
        updateChatbox(`You: ${userMessage}`, "user");
        updateChatbox(`AI: ${data.response}`, "bot");

        document.getElementById('user-message').value = '';
    } catch (error) {
        console.error("Chatbot error:", error);
        updateChatbox("⚠️ AI is not responding. Please try again later.", "error");
    }
}

// ✅ Update chatbox with messages
function updateChatbox(message, type) {
    const chatbox = document.getElementById('chatbox');
    const messageElement = document.createElement('p');
    messageElement.textContent = message;

    if (type === "user") messageElement.style.fontWeight = "bold";
    else if (type === "bot") messageElement.style.color = "blue";
    else messageElement.style.color = "red";

    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

// ✅ Event listeners

// Send message button
document.getElementById('send-message').addEventListener('click', fetchChatbotResponse);

// Press Enter key to send message
document.getElementById('user-message').addEventListener('keypress', function (event) {
    if (event.key === "Enter") fetchChatbotResponse();
});

// ✅ Workout recommendation button event listener
document.getElementById('fetch-workout-btn').addEventListener('click', fetchWorkoutRecommendation);

// ✅ Meal recommendation button event listener
document.getElementById('fetch-meal-btn').addEventListener('click', fetchMealRecommendation);

async function logWorkout() {
    const csrftoken = getCookie('csrftoken');

    const data = {
        exercise: document.getElementById('exercise-name').value,
        sets: document.getElementById('sets').value,
        reps: document.getElementById('reps').value,
        duration: document.getElementById('duration').value
    };

    try {
        const response = await fetch('/api/log_workout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        document.getElementById('log-workout-result').textContent = result.message || result.error;
    } catch (error) {
        console.error("Error logging workout:", error);
        document.getElementById('log-workout-result').textContent = "⚠️ Error logging workout.";
    }
}

document.getElementById('log-workout-btn').addEventListener('click', logWorkout);




async function fetchWorkoutProgress() {
    try {
        const response = await fetch('/api/workout_progress/');
        const data = await response.json();

        document.getElementById('progress-suggestion').textContent = data.suggestion || data.error;
    } catch (error) {
        console.error("Progress fetch error:", error);
        document.getElementById('progress-suggestion').textContent = "⚠️ Error fetching progress suggestion.";
    }
}

document.getElementById('get-progress-btn').addEventListener('click', fetchWorkoutProgress);

async function renderWorkoutChart() {
    try {
        const response = await fetch('/api/workout_chart/');
        const data = await response.json();

        console.log("🔥 Chart Data:", data); // For debugging

        const ctx = document.getElementById('progressChart')?.getContext('2d');
        if (!ctx) {
            console.error("❌ progressChart canvas not found!");
            return;
        }

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Reps',
                        data: data.reps,
                        borderColor: 'blue',
                        fill: false,
                        tension: 0.3
                    },
                    {
                        label: 'Sets',
                        data: data.sets,
                        borderColor: 'green',
                        fill: false,
                        tension: 0.3
                    },
                    {
                        label: 'Duration (min)',
                        data: data.duration,
                        borderColor: 'orange',
                        fill: false,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '📈 Workout Progress Over Time'
                    }
                }
            }
        });
    } catch (error) {
        console.error("Chart load error:", error);
    }
}

window.addEventListener('load', renderWorkoutChart);


// Auto-render chart on page load
window.addEventListener('load', renderWorkoutChart);
