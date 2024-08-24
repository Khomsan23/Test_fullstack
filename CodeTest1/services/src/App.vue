<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <span class="shrink mr-2"> Parts Change over matrix </span>
      </div>
    </v-app-bar>
    <v-main>
      <v-container>
        <HomeView />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import HomeView from "./views/HomeView.vue";

export default {
  name: "App",
  components: {
    HomeView,
  },
};
</script>

<style>
/* Add any styles here */
</style>
