import { defineConfig, type DefaultTheme } from 'vitepress'
import {version} from "./global";

export const en = defineConfig({
    lang: 'en-US',
    description: 'Asynchronous strict-typed VTubeStudio API framework ',

    themeConfig: {
        nav: nav(),

        sidebar: {
            '/guide/': { base: '/guide/', items: sidebarGuide() },
        },

        editLink: {
            pattern: 'https://github.com/timtaran-vts-api/edit/dev/docs/:path',
            text: 'Edit this page on GitHub'
        },

        footer: {
            message: 'Released under the MIT License.',
            copyright: 'Copyright © 2024 Timtaran'
        }
    }
})

function nav(): DefaultTheme.NavItem[] {
    return [
        {
            text: 'Guide',
            link: '/guide/about-vts',
            activeMatch: '/guide/'
        },
        {
            text: version,
            items: [
                {
                    text: 'Changelog',
                    link: 'https://github.com/timtaran/vts-api/blob/dev/CHANGELOG.md'
                },
                {
                    text: 'Contributing',
                    link: 'https://github.com/timtaran/vts-api/blob/dev/.github/contributing.md'
                }
            ]
        }
    ]
}

function sidebarGuide(): DefaultTheme.SidebarItem[] {
    return [
        {
            text: 'Introduction',
            collapsed: false,
            items: [
                { text: 'What is VTubeStudio?', link: 'about-vts' },
                { text: 'Getting Started', link: 'getting-started' },
            ]
        },
        // { text: 'API Reference', base: '/reference/', link: 'site-config' }
    ]
}
