<script setup>
import { ref } from "vue";
import { usePostsStore } from "../stores/posts";

const titleModel = ref("");
const contentModel = ref("");
const creatingPost = ref(false);

const { createPost } = usePostsStore();

const newPost = async () => {
  creatingPost.value = true;
  await createPost(titleModel.value, contentModel.value);
  creatingPost.value = false;
};
</script>

<template>
  <label>What's happening?</label> <br />
  <input type="text" placeholder="Title" v-model="titleModel" />
  <textarea rows="6" placeholder="Content" v-model="contentModel"></textarea>
  <br />
  <button @click="newPost" :disabled="creatingPost">Publish Post</button>
</template>
