import { MOBILE_BREAKPOINT, useIsMobile } from '~/composables/useIsMobile'

export default defineNuxtPlugin({
  name: 'mobile-detect',
  enforce: 'pre',
  setup() {
    const isMobile = useIsMobile()

    const apply = () => {
      const mobile = window.innerWidth <= MOBILE_BREAKPOINT
      isMobile.value = mobile
      document.documentElement.classList.toggle('is-mobile', mobile)
    }

    apply()
    window.addEventListener('resize', apply, { passive: true })
  }
})
