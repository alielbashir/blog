<script setup>
import { storeToRefs } from "pinia";
import { usePostsStore } from "../stores/posts";
import BlogPost from "../components/BlogPost.vue";
import { watch, ref } from "vue";

const store = usePostsStore();

const { updatingToggle, posts, voteSortedPosts, dateSortedPosts } =
  storeToRefs(store);

const { fetchPosts } = store;

const sortModel = ref("date");
const sortOrderModel = ref("asc");

watch([sortModel, sortOrderModel], () => {
  switch (sortModel.value) {
    case "votes":
      posts.value =
        sortOrderModel.value === "desc"
          ? [...voteSortedPosts.value]
          : [...voteSortedPosts.value].reverse();
      break;
    case "date":
      posts.value =
        sortOrderModel.value === "desc"
          ? [...dateSortedPosts.value]
          : [...dateSortedPosts.value].reverse();
      break;
    default:
      break;
  }
});
watch(updatingToggle, fetchPosts);
fetchPosts();
</script>

<template>
  <section>
    <br />
    <label>Sort by:</label><br />
    <label
      ><input
        checked="checked"
        name="sorting"
        type="radio"
        value="date"
        v-model="sortModel"
      />
      Date</label
    >
    <br />
    <label
      ><input name="sorting" type="radio" value="votes" v-model="sortModel" />
      Votes</label
    >
    <br />
    <br />
    <label>Order: </label><br />
    <label
      ><input
        checked="checked"
        name="order"
        type="radio"
        value="asc"
        v-model="sortOrderModel"
      />
      Ascending</label
    >
    <br />
    <label
      ><input name="order" type="radio" value="desc" v-model="sortOrderModel" />
      Descending</label
    >
    <br />
    <div v-for="post in posts" :key="post.id">
      <BlogPost :post="post" />
    </div>
  </section>
</template>
