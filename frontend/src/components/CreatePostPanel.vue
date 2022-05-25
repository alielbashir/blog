<script setup>
import { ref } from "vue";

const titleModel = ref("");
const contentModel = ref("");
</script>

<template>
  <p>
    <label>What's happening?</label> <br />
    <input type="text" placeholder="Title" v-model="titleModel" />
    <textarea rows="6" placeholder="Content" v-model="contentModel"></textarea>
  </p>
</template>
