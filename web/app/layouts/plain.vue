<template>
  <div class="layout-container">
    <main class="main-content" role="main">
      <slot />
    </main>

    <footer class="footer" role="contentinfo">
      <div class="footer-content">
        <p>&copy; 2025 行书子. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
}

.footer {
  background-color: #f5f5f5;
  padding: 2rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
  color: #666;
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
}
</style>
