<template>
  <div>
    <h2>Mood Predictor</h2>
    <input type="date" v-model="date"/>
    <input type="number" v-model="sleep_hours" placeholder="Hours of Sleep" />
    <input type="number" v-model="stress_level" placeholder="Stress Level (1-10)" />
    <input type="number" v-model="calories_burned" placeholder="Calories Burned" />
    <button @click="predictMood">Predict Mood</button>
    <h3 v-if="predictedMood !== null">Predicted Mood: {{ predictedMood }}</h3>

    <h2>Past Predictions</h2>
    <table v-if="pastPredictions && pastPredictions.length > 0">
      <thead>
        <tr>
          <th>Sleep Hours</th>
          <th>Stress Level</th>
          <th>Calories Burned</th>
          <th>Predicted Mood</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prediction in filteredPredictions" :key="prediction.id">
          <td>{{ prediction.date }}</td>
          <td>{{ prediction.sleep_hours }}</td>
          <td>{{ prediction.stress_level }}</td>
          <td>{{ prediction.calories_burned }}</td>
          <td>{{ prediction.predicted_mood }}</td>
          <td>
            <button @click="deletePrediction(prediction.id)">Delete</button>
          </td>
        </tr>

      </tbody>
    </table>
    <p v-else>No predictions available.</p>

    <!-- <MoodPredictor />

    <MoodCharts /> -->
  </div>
</template>

<script>
import axios from "axios";

// import MoodPredictor from ".components/MoodPredictor.vue";
// import MoodCharts from "./components/MoodCharts.vue";

export default {
  // components: {
  //   MoodPredictor,
  //   MoodCharts
  // },
  data() {
    return {
      date: new Date().toISOString().split('T')[0],
      sleep_hours: null,
      stress_level: null,
      calories_burned: null,
      predictedMood: null,
      pastPredictions: []
    };
  },
  methods: 
  {
    async fetchPastPredictions() { //every time the user sends a prediction request, this is loaded with the new information, and refreshing the past predictions data.
      try {
        const response = await axios.get("http://127.0.0.1:8000/predictions");
        this.pastPredictions = response.data || [];
      } catch (error) {
        console.error("Error fetching past predictions,:", error);
      }
    },

    async predictMood() {

      if (this.sleep_hours < 1 || this.stress_level < 1 || this.calories_burned < 0 ||
        this.sleep_hours == null || this.stress_level == null || this.calories_burned == null) {
        alert("Sleep hours must be at least 1 hour, and all inputs must be positive numbers and not empty!");
        return;
        }


      try {
        console.log("Sending data to FastAPI:", {
          date: this.date,
          sleep_hours: this.sleep_hours,
          stress_level: this.stress_level,
          calories_burned: this.calories_burned
        });

        const response = await axios.post("http://127.0.0.1:8000/predict", {
          date: this.date,
          sleep_hours: this.sleep_hours || 0, // if no number introduced, then 0
          stress_level: this.stress_level || 0,
          calories_burned: this.calories_burned || 0,
        });

        console.log("Response from FastAPI:", response.data);
        this.predictedMood = response.data.predicted_mood;

        this.fetchPastPredictions();

        } catch (error) {
          console.error("Error fetching prediction:", error);
          alert("Failed to get prediction. Please try again later.");
        }
      },

      async deletePrediction(id) {
        try {
          await axios.delete(`http://127.0.0.1:8000/predictions/${id}`);
          alert('Prediction deleted successfully');
          this.fetchPastPredictions();  // Refresh predictions after deletion
        } catch (error) {
          console.error('Error deleting prediction:', error);
          alert('Failed to delete prediction');
        }
      },

    },

    mounted() {
      this.fetchPastPredictions(); // Fetch past predictions on page load
    },

    computed: {
      filteredPredictions() {
        return this.pastPredictions.filter(p => p && p.sleep_hours !== undefined);
      }
    },

  };
</script>

