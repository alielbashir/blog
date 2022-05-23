<script setup>
import { ref } from "vue";
import axios from "axios";
import router from "../router";

// FIXME: find way to store this globally
//        maybe use state management framework (pinia?)
const API_URL = import.meta.env.VITE_API_URL;

const usernameModel = ref("");
const passwordModel = ref("");
const confirmPasswordModel = ref("");
const writeScopeModel = ref(false);

const register = async () => {
  if (passwordModel.value !== confirmPasswordModel.value) {
    alert("Passwords do not match");
    return;
  }

  try {
    const res = await axios.post(`${API_URL}/users/register`, {
      username: usernameModel.value,
      password: passwordModel.value,
      scope: writeScopeModel.value ? "write" : "read",
    });
    if (res.status === 201) {
      router.push("/");
    }
  } catch (error) {
    alert("Sign up failed");
    console.log(error.response.data.error);
  }
};
</script>

<template>
  <main>
    <form @submit.prevent="register">
      <h1>Please sign up</h1>
      <div>
        <input
          type="text"
          required
          placeholder="Username"
          v-model="usernameModel"
        />
      </div>
      <div>
        <input
          type="password"
          required
          placeholder="Password"
          v-model="passwordModel"
        />
      </div>
      <div>
        <input
          type="password"
          required
          placeholder="Confirm Password"
          v-model="confirmPasswordModel"
        />
      </div>

      <div>
        <input type="checkbox" id="checkbox" v-model="writeScopeModel" />
        <label for="checkbox">I'm a writer</label>
      </div>
      <button type="submit">Sign up</button>
    </form>
    <button @click="router.push('/')">Already have an account? Sign in</button>
  </main>
</template>
