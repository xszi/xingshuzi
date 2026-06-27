import { detectMobileFromUA, useIsMobile } from '~/composables/useIsMobile'

export default defineNuxtPlugin(() => {
  const headers = useRequestHeaders(['user-agent'])
  const isMobile = useIsMobile()
  isMobile.value = detectMobileFromUA(headers['user-agent'] || '')
})
