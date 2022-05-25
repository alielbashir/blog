<script setup>
import { storeToRefs } from "pinia";
import { usePostsStore } from "../stores/posts";
import BlogPost from "../components/BlogPost.vue";
import { watch } from "vue";
import { computed } from "@vue/reactivity";

const store = usePostsStore();

const { updatingToggle } = storeToRefs(store);

const { fetchPosts } = store;
const dateSortedPosts = computed(() => store.dateSortedPosts);
const voteSortedPosts = computed(() => store.voteSortedPosts);

watch(updatingToggle, fetchPosts);
fetchPosts();
</script>

<template>
  <div>
    <div v-for="post in dateSortedPosts" :key="post.id">
      <BlogPost :post="post" />
    </div>
  </div>
</template>
