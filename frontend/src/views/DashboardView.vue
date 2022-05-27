<script setup>
import CreatePostPanel from "../components/CreatePostPanel.vue";
import BlogPostList from "../components/BlogPostList.vue";

import { useUsersStore } from "../stores/users";

const user = useUsersStore();
</script>

<template>
  <div>
    <h1>Welcome to Blog, {{ user.username }}!</h1>

    <CreatePostPanel v-if="user.isWriter" />
    <BlogPostList />
  </div>
</template>
