<template>
  <div id="app">
    <h1>Mood Predictor</h1>
    <MoodPredictor />
    <MoodCharts />
  </div>
</template>

<script>
import MoodPredictor from "@/components/MoodPredictor.vue";
import MoodCharts from "@/components/MoodCharts.vue";

export default {
  components: {
    MoodPredictor,
    MoodCharts
  }
};
</script>


