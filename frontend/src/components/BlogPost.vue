<script setup>
import { ref } from "vue";
import axios from "axios";

const props = defineProps({
  post: {
    id: Number,
    title: String,
    username: String,
    content: String,
    creation_date: Number,
    votes: Number,
  },
});

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
  return "less than a second";
}

const hasUpvoted = ref(props.post.has_upvoted);
const hasDownvoted = ref(props.post.has_downvoted);
const voting = ref(false);
const votes = ref(props.post.votes);

const API_URL = import.meta.env.VITE_API_URL;

const upvote = async () => {
  try {
    voting.value = true;

    const { data } = await axios.post(
      `${API_URL}/posts/${props.post.id}/upvote`,
      {}, // post requests need body, config is 3rd parameter
      {
        headers: {
          Authorization: "Bearer " + sessionStorage.token,
        },
      }
    );

    hasUpvoted.value = data.has_upvoted;
    hasDownvoted.value = data.has_downvoted;
    console.log(`hasUpvoted = ${hasUpvoted.value}`);
    console.log(`hasDownvoted = ${hasDownvoted.value}`);
    votes.value = data.votes;
  } catch (error) {
    console.log(error);
  } finally {
    voting.value = false;
  }
};

const downvote = async () => {
  try {
    voting.value = true;

    const { data } = await axios.post(
      `${API_URL}/posts/${props.post.id}/downvote`,
      {}, // post requests need body, config is 3rd parameter
      {
        headers: {
          Authorization: "Bearer " + sessionStorage.token,
        },
      }
    );

    hasUpvoted.value = data.has_upvoted;
    hasDownvoted.value = data.has_downvoted;
    votes.value = data.votes;
    console.log(`hasUpvoted = ${hasUpvoted.value}`);
    console.log(`hasDownvoted = ${hasDownvoted.value}`);
  } catch (error) {
    console.log(error);
  } finally {
    voting.value = false;
  }
};
</script>

<template>
  <section>
    <table cellspacing="0" cellpadding="0">
      <tr>
        <td>
          <tr>
            <button
              :class="{ voted: hasUpvoted }"
              :disabled="voting"
              @click="upvote"
            >
              Δ
            </button>
          </tr>
          <p style="text-align: center">{{ votes }}</p>
          <tr>
            <button
              :class="{ voted: hasDownvoted }"
              :disabled="voting"
              @click="downvote"
            >
              ∇
            </button>
          </tr>
        </td>
        <td>
          <h3>{{ post.title }}</h3>
        </td>
      </tr>
    </table>

    <h5>By @{{ post.username }}</h5>
    <p>
      {{ post.content }}
    </p>
    <p>{{ millisecondsToStr(post.creation_date) }} ago</p>
  </section>
</template>

<style>
table,
tr,
td {
  border: none;
  padding: 0%;
}

button {
  background-color: gray;
}

.voted {
  background-color: orange;
}
</style>
