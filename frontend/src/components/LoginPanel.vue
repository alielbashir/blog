<script setup>
import { ref } from "vue";
import axios from "axios";
import router from "../router";

// FIXME: find way to store this globally
//        maybe use state management framework (pinia?)
const API_URL = import.meta.env.VITE_API_URL;

const usernameModel = ref("");
const passwordModel = ref("");

const login = async () => {
  if (passwordModel.value.length === 0) {
    alert("Passwords do not match");
    return;
  }

  try {
    const res = await axios.post(`${API_URL}/users/login`, {
      username: usernameModel.value,
      password: passwordModel.value,
    });

    // store token in session storage

    sessionStorage.token = res.data.token;
    router.push("dashboard");
  } catch (error) {
    alert("Incorrect username and/or password");
  }
};
</script>

<template>
  <main>
    <form @submit.prevent="login">
      <h1>Please sign in</h1>
      <div>
        <input
          id="floatingInput"
          type="text"
          required
          placeholder="Username"
          v-model="usernameModel"
        />
      </div>
      <div>
        <input
          id="floatingPassword"
          type="password"
          required
          placeholder="Password"
          v-model="passwordModel"
        />
      </div>

      <button type="submit">Sign in</button>
    </form>
    <button @click="router.push('register')">Create an account</button>
  </main>
</template>
