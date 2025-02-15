<template>
  <div>
    <h2>Mood Predictor</h2>
    <input type="number" v-model="sleep_hours" placeholder="Hours of Sleep" />
    <input type="number" v-model="stress_level" placeholder="Stress Level (1-10)" />
    <input type="number" v-model="calories_burned" placeholder="Calories Burned" />
    <button @click="predictMood">Predict Mood</button>
    <h3 v-if="predictedMood !== null">Predicted Mood: {{ predictedMood }}</h3>

    <h2>Past Predictions</h2>
    <table v-if="pastPredictions.length">
      <thead>
        <tr>
          <th>Sleep Hours</th>
          <th>Stress Level</th>
          <th>Calories Burned</th>
          <th>Predicted Mood</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(pred, index) in pastPredictions" :key="index">
          <td>{{ pred.sleep_hours }}</td>
          <td>{{ pred.stress_level }}</td>
          <td>{{ pred.calories_burned }}</td>
          <td>{{ pred.predicted_mood }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      sleep_hours: null,
      stress_level: null,
      calories_burned: null,
      predictedMood: null,
      pastPredictions: []
    };
  },
  methods: 
  {
    async fetchPastPredictions() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/predictions");
        this.pastPredictions = response.data;
      } catch (error) {
        console.error("Error fetching past predictions:", error);
      }
    },

    async predictMood() {
        try {
          console.log("Sending data to FastAPI:", {
            sleep_hours: this.sleep_hours,
            stress_level: this.stress_level,
            calories_burned: this.calories_burned
          });

          const response = await axios.post("http://127.0.0.1:8000/predict", {
            sleep_hours: this.sleep_hours || 0, // if no number introduced, then 0
            stress_level: this.stress_level || 0,
            calories_burned: this.calories_burned || 0,
          });

          console.log("Response from FastAPI:", response.data);
          this.predictedMood = response.data.predicted_mood;

          this.fetchPastPredictions();

          } catch (error) {
            console.error("Error fetching prediction:", error);
          }
        },
      },

      mounted() {
        this.fetchPastPredictions(); // Fetch past predictions on page load
      }
    };
</script>

