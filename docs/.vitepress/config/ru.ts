import {defineConfig, type DefaultTheme} from 'vitepress'
import {version} from "./global";

export const ru = defineConfig({
        lang: 'ru-RU',
        description: 'Асинхронный строго-типизированный фреймворк для VTubeStudio API ',

        themeConfig: {
            nav: nav(),

            sidebar: {
                '/ru/guide/': {base: '/ru/guide/', items: sidebarGuide()},
            },

            editLink: {
                pattern: 'https://github.com/timtaran-vts-api/edit/dev/docs/:path',
                text: 'Редактировать страницу'
            },

            footer: {
                message: 'Опубликовано под лицензией MIT.',
                copyright: '© 2024, Timtaran'
            },

            outline: {label: 'Содержание страницы'},

            docFooter: {
                prev: 'Предыдущая страница',
                next: 'Следующая страница'
            },

            lastUpdated: {
                text: 'Обновлено'
            },

            darkModeSwitchLabel: 'Оформление',
            lightModeSwitchTitle: 'Переключить на светлую тему',
            darkModeSwitchTitle: 'Переключить на тёмную тему',
            sidebarMenuLabel: 'Меню',
            returnToTopLabel: 'Вернуться к началу',
            langMenuLabel: 'Изменить язык'
        }
    })

function nav(): DefaultTheme.NavItem[] {
    return [
        {
            text: 'Руководство',
            link: '/ru/guide/about-vts',
            activeMatch: '/ru/guide/'
        },
        {
            text: version,
            items: [
                {
                    text: 'Изменения',
                    link: 'https://github.com/timtaran/vts-api/blob/dev/CHANGELOG.md'
                },
                {
                    text: 'Вклад',
                    link: 'https://github.com/timtaran/vts-api/blob/dev/.github/contributing.md'
                }
            ]
        }
    ]
}

function sidebarGuide(): DefaultTheme.SidebarItem[] {
    return [
        {
            text: 'Введение',
            collapsed: false,
            items: [
                {text: 'Что такое VTubeStudio?', link: 'about-vts'},
                {text: 'Первые шаги', link: 'getting-started'},
            ]
        },
        // {text: 'Справка по API', base: '/ru/reference/', link: 'site-config'}
    ]
}

export const search: DefaultTheme.AlgoliaSearchOptions['locales'] = {
    ru: {
        placeholder: 'Поиск в документации',
        translations: {
            button: {
                buttonText: 'Поиск',
                buttonAriaLabel: 'Поиск'
            },
            modal: {
                searchBox: {
                    resetButtonTitle: 'Сбросить поиск',
                    resetButtonAriaLabel: 'Сбросить поиск',
                    cancelButtonText: 'Отменить поиск',
                    cancelButtonAriaLabel: 'Отменить поиск'
                },
                startScreen: {
                    recentSearchesTitle: 'История поиска',
                    noRecentSearchesText: 'Нет истории поиска',
                    saveRecentSearchButtonTitle: 'Сохранить в истории поиска',
                    removeRecentSearchButtonTitle: 'Удалить из истории поиска',
                    favoriteSearchesTitle: 'Избранное',
                    removeFavoriteSearchButtonTitle: 'Удалить из избранного'
                },
                errorScreen: {
                    titleText: 'Невозможно получить результаты',
                    helpText: 'Вам может потребоваться проверить подключение к Интернету'
                },
                footer: {
                    selectText: 'выбрать',
                    navigateText: 'перейти',
                    closeText: 'закрыть',
                    searchByText: 'поставщик поиска'
                },
                noResultsScreen: {
                    noResultsText: 'Нет результатов для',
                    suggestedQueryText: 'Вы можете попытаться узнать',
                    reportMissingResultsText:
                        'Считаете, что поиск даёт ложные результаты？',
                    reportMissingResultsLinkText: 'Нажмите на кнопку «Обратная связь»'
                }
            }
        }
    }
}