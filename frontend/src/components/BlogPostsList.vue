<script setup>
import { storeToRefs } from "pinia";
import { usePostsStore } from "../stores/posts";

function millisecondsToStr(epochTime) {
  // adapted from https://stackoverflow.com/a/8212878/13886854

  // same time zone is assumed
  const time_diff = new Date().getTime() - epochTime * 1000;

  function numberEnding(number) {
    return number > 1 ? "s" : "";
  }

  var temp = Math.floor(time_diff / 1000);
  var years = Math.floor(temp / 31536000);
  if (years) {
    return years + " year" + numberEnding(years);
  }
  //TODO: Months! Maybe weeks?
  var days = Math.floor((temp %= 31536000) / 86400);
  if (days) {
    return days + " day" + numberEnding(days);
  }
  var hours = Math.floor((temp %= 86400) / 3600);
  if (hours) {
    return hours + " hour" + numberEnding(hours);
  }
  var minutes = Math.floor((temp %= 3600) / 60);
  if (minutes) {
    return minutes + " minute" + numberEnding(minutes);
  }
  var seconds = temp % 60;
  if (seconds) {
    return seconds + " second" + numberEnding(seconds);
  }
  return "less than a second"; //'just now' //or other string you like;
}

const store = usePostsStore();
const { posts } = storeToRefs(store);
const { getPosts } = store;

getPosts();
console.log(posts.value);
</script>

<template>
  <div>
    <div v-for="post in posts" :key="post.id">
      <h3>{{ post.title }}</h3>
      <p>
        {{ post.content }}
      </p>
      <h6>
        written by: {{ post.username }}
        {{ millisecondsToStr(post.creation_date) }} ago
      </h6>
    </div>
  </div>
</template>
