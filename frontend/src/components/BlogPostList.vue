<script setup>
import { storeToRefs } from "pinia";
import { usePostsStore } from "../stores/posts";
import BlogPost from "../components/BlogPost.vue";

const store = usePostsStore();
const { posts } = storeToRefs(store);
const { getPosts } = store;

getPosts();
console.log(posts.value);
</script>

<template>
  <div>
    <div v-for="post in posts" :key="post.id">
      <BlogPost :post="post" />
    </div>
  </div>
</template>
