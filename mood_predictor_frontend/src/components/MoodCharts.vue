<template>
  <div>
    <h2>Mood input score trend over time</h2>
    <canvas ref="moodChart"></canvas>

    <h2>Sleep hours vs. Mood Score</h2>
    <canvas ref="sleepMoodChart"></canvas>
  </div>
  <h3>Mood Score Trend</h3>
    <Line v-if="chartData" :data="chartData" />
</template>

<script>
  import axios from 'axios';
  import { Chart, registerables } from 'chart.js';
  import { Line } from 'vue-chartjs';
  import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";
  
  Chart.register(...registerables);
  ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

  export default {
    components: {Line,},
    props: {
      moodData: Array,
    },
    data() {
      return {
        moodData: [],
        moodChart: null,
        sleepMoodChart: null,

        chartData: {
          labels: [],
          datasets: [
            {
              label: "Mood Score Trend",
              data: [],
              borderColor: "rgb(75, 192, 192)",
              fill: false,
            }
          ]
        },
        chartOptions: {
          responsive: true
        }
      };
    },
    async mounted() {
      await this.fetchMoodData();
      this.renderMoodChart();
      this.renderSleepMoodChart();
    },
    methods: {
      async fetchMoodData() {
        try {
          const response = await axios.get("http://127.0.0.1:8000/predictions");
          this.moodData = response.data.map(item => ({
            date: item.date,
            mood_score: item.predicted_mood,
            sleep_hours: item.sleep_hours
          }));
        } catch (error) {
          console.error("Error fetching mood data:", error);
        }
      },
      renderMoodChart() {
        const ctx = this.$refs.moodChart.getContext("2d");
        new Chart(ctx, {
          type: "line",
          data: {
            labels: this.moodData.map( d => d.date),
            datasets: [
              {
                label: "Mood Score",
                data: this.moodData.map(d => d.mood_score),
                borderColor: "blue",
                backgroundColor: "rgba(0,0,255,0.2)",
                fill: true,
              }
            ]
          },
          options: {
            responsive: true,
            scales: {
              x: {title: {display: true, text: "Date"}},
              y: {title: {display: true, text: "Mood Score"}, min: 1, max:10},
            }
          }
        });
      },
      renderSleepMoodChart() {
        const ctx = this.$refs.sleepMoodChart.getContext("2d");
        new Chart(ctx, {
          type: "scatter",
          data: {
            datasets: [
              {
                label:"Sleep vs Mood",
                data: this.moodData.map(d => ({x:d.sleep_hours, y: d.mood_score})),
                backgroundColor: "red"
              }
            ]
          },
          options: {
            responsive: true,
            scales: {
              x: {title: {display: true, text: "Sleep Hours"}, min: 0, max: 12},
              y: {title: {display: true, text: "Mood Score"}, min: 1, max:10},
            }
          }
        });
      },
      updateChart(newData) {
        this.chartData.labels = newData.map((entry) => entry.date);
      }
    }
  };
</script>