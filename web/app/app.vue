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

/* iOS：输入框字号 < 16px 会聚焦时自动放大页面，导致横向溢出 */
html.is-mobile {
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}

html.is-mobile input,
html.is-mobile textarea,
html.is-mobile select,
html.is-mobile .el-input__inner,
html.is-mobile .el-textarea__inner,
html.is-mobile .el-select__wrapper,
html.is-mobile .el-select__placeholder,
html.is-mobile .el-select__selected-item,
html.is-mobile .el-input__wrapper {
  font-size: 16px !important;
  line-height: 1.5;
}

html.is-mobile body {
  overscroll-behavior-x: none;
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

