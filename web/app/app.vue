<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html.is-mobile .week-wrapper,
html.is-mobile .schedule-panel {
  padding: 0.75rem;
}

html, body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f9fafb;
  overflow-x: hidden;
  max-width: 100%;
}

#__nuxt {
  min-height: 100vh;
  overflow-x: hidden;
  max-width: 100%;
}

/* 确保复制/保存等提示浮层在最上层可见 */
.el-message,
.el-notification {
  z-index: 10001 !important;
}
</style>

