import { defineConfig } from 'vitepress'
import { search as ruSearch } from "./ru";

// https://vitepress.dev/reference/site-config
export const shared = defineConfig({
  title: "VTS API",
  description: "Asynchronous strict-typed VTubeStudio API framework ",
  cleanUrls: true,

  base: "/vts-api/",
  head: [['link', { rel: 'icon', href: '/favicon.ico' }]],

  rewrites: {
    'en/:rest*': ':rest*'
  },

  themeConfig: {
    socialLinks: [
      { icon: 'github', link: 'https://github.com/timtaran/vts-api' }
    ],

    search: {
      provider: 'local',
      options: {
        locales: { ...ruSearch }
      }
    }
  }
})
