<template>
  <div class="register-view">
    <p>注册页面 - 请使用登录页面</p>
    <router-link to="/auth/login">前往登录</router-link>
  </div>
</template>

<style scoped lang="scss">
.register-view {
  text-align: center;
  color: var(--text-secondary);

  a {
    color: var(--color-primary-light);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
