const MOBILE_MAX_WIDTH = 768

export function detectMobileFromUA(ua: string): boolean {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile/i.test(ua)
}

/** 全局移动端状态（SSR 用 UA 预判，客户端立即按视口校正） */
export const useIsMobile = () => {
  return useState<boolean>('is-mobile', () => false)
}

export const MOBILE_BREAKPOINT = MOBILE_MAX_WIDTH
