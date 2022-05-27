<script setup>
import { useUsersStore } from "../stores/users";
import router from "../router";

const store = useUsersStore();

const logout = () => {
  store.logoutUser();
  router.push("/");
};
</script>
<template>
  <button @click="logout">LOGOUT</button>
</template>
