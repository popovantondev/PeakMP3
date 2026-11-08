"""Shared-kit parts of the PeakMP3 pages: header, footer, release pill, source button, bento.

The page skin (wood frame, instrument panels) stays PeakMP3's own; only the navigation and the
common blocks come from assets/kit (copied from the profile site). All texts live here, German on "Sie".
"""
from html import escape as e
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
LANGS = ('ru', 'de', 'en')
SITE = 'https://popovantondev.github.io/'
PROFILE = SITE + 'popovantondev/'
LANDING = {'ru': 'index-ru.html', 'de': 'index.html', 'en': 'index-en.html'}
CATALOG = {'ru': PROFILE + 'index-ru.html', 'de': PROFILE + 'index.html', 'en': PROFILE + 'index-en.html'}
RELEASE = json.loads((R / 'public-release.json').read_text(encoding='utf-8'))
STACK = 'C# · .NET'  # catalog_stacks['PeakMP3'] in the profile
SETUP = 'YouTubeDownloader-PeakMP3-2.6.0-Preview-Setup.exe'
SITE_REV = '2026.11.06-perf'  # ?v= of website/*.css and demo.js: raise it when they change, or browsers keep the old copy


def kit_version():
    return (R / 'assets/kit/KIT_VERSION').read_text(encoding='utf-8').strip()


def page_name(kind, lang):
    return LANDING[lang] if kind == 'home' else 'Guide-' + lang + '.html'


TEXT = {
 'ru': dict(nav='Основная навигация', all='Все программы', search='Поиск', kbd='Ctrl K', search_label='Поиск по программам',
            theme='Сменить тему', legal='Правовая информация', new='НОВОЕ', pill='Вышла предварительная версия {v}',
            more='Что нового →', source='Исходный код', terms='Условия использования',
            bento='Что внутри', bento_sub='Установка, функции, данные, проверка.', inst='Установка',
            inst_sub='Сверить контрольную сумму, запустить установщик, открыть PeakMP3.', terminal='Терминал',
            feat='Функции', checked='Проверено',
            local_title='Работает локально',
            local_text='PeakMP3 обрабатывает аудиофайлы на вашем компьютере. Примеры на этой странице подготовлены заранее, ваши файлы в браузере не обрабатываются. Демо запоминает только выбранное значение калибровки VU: оно хранится лишь в вашем браузере (localStorage) и никуда не передаётся.',
            local_live='Локально · офлайн',
            t_hash='Сверить SHA-256 с файлом SHA256SUMS.txt из выпуска', t_setup='Установка в профиль пользователя, без прав администратора',
            t_start='Запустить PeakMP3 с рабочего стола, перетащить аудиофайлы',
            features=['Плотность 0–10', 'Сравнение A/B', 'Волна и пластинка', 'Очередь файлов', 'Калибровка VU', 'MP3 320', 'AAC · WAV · FLAC', 'Windows 7 SP1'],
            checks=['GitHub Actions: сборка сайта, проверка страниц и сборка для Windows при каждой отправке',
                    '33 музыкальных примера с контрольными суммами SHA-256 (music/SHA256SUMS.txt)',
                    'Контрольные суммы SHA-256 общего установщика в выпуске (SHA256SUMS.txt)',
                    'Музыка под CC BY 4.0 с указанием авторов (music/CREDITS.md)',
                    'Windows 7 и 11 подтверждены пользователем; Windows 10 отдельно не проверялась'],
            installer='Установщик лежит в выпуске YouTube Downloader: обе программы ставятся вместе, отдельного выпуска у PeakMP3 нет.',
            installer_link='Выпуск YouTube Downloader 2.6.0',
            description='Плотность звука, сравнение A/B и сохранение MP3 320 для Windows. Аналоговое управление, как на приборе.',
            title_home='PeakMP3 — плотность звука, сравнение A/B, MP3 320', title_guide='PeakMP3 — Руководство',
            redirect_title='PeakMP3 — переход на немецкую страницу', redirect_text='Перейти на немецкую страницу'),
 'de': dict(nav='Hauptnavigation', all='Alle Programme', search='Suchen', kbd='Strg K', search_label='Programme durchsuchen',
            theme='Farbschema wechseln', legal='Rechtliches', new='NEU', pill='Vorabversion {v} ist da',
            more='Was ist neu →', source='Quellcode', terms='Nutzungsbedingungen',
            bento='Was drin steckt', bento_sub='Installation, Funktionen, Datenschutz, Prüfung.', inst='Installation',
            inst_sub='Prüfsumme vergleichen, Setup starten, PeakMP3 öffnen.', terminal='Terminal',
            feat='Funktionen', checked='Geprüft',
            local_title='Läuft lokal',
            local_text='PeakMP3 bearbeitet Audiodateien auf Ihrem PC. Die Hörbeispiele auf dieser Seite sind vorbereitet; Ihre Dateien werden im Browser nicht verarbeitet. Die Demo merkt sich nur den eingestellten Wert der VU-Kalibrierung, ausschließlich lokal in Ihrem Browser (localStorage); er wird nicht übertragen.',
            local_live='Lokal · offline',
            t_hash='SHA-256 mit SHA256SUMS.txt aus dem Release vergleichen', t_setup='Installation im Benutzerprofil, ohne Administratorrechte',
            t_start='PeakMP3 vom Desktop starten, Audiodateien hineinziehen',
            features=['Dichte 0–10', 'A/B-Vergleich', 'Wellenform & Schallplatte', 'Warteschlange', 'VU-Kalibrierung', 'MP3 320', 'AAC · WAV · FLAC', 'Windows 7 SP1'],
            checks=['GitHub Actions: Website-Build, Seitenprüfung und Windows-Build bei jedem Push',
                    '33 Hörbeispiele mit SHA-256-Prüfsummen (music/SHA256SUMS.txt)',
                    'SHA-256-Prüfsummen für das gemeinsame Setup im Release (SHA256SUMS.txt)',
                    'Musik unter CC BY 4.0 mit Nachweis (music/CREDITS.md)',
                    'Windows 7 und 11 vom Anwender bestätigt; Windows 10 nicht separat geprüft'],
            installer='Das Setup liegt im Release von YouTube Downloader: Beide Programme werden gemeinsam installiert, ein eigenes PeakMP3-Release gibt es nicht.',
            installer_link='Release YouTube Downloader 2.6.0',
            description='Dichte einstellen, A/B vergleichen und MP3 320 speichern, unter Windows. Analoge Bedienung wie am Gerät.',
            title_home='PeakMP3 — Dichte einstellen, A/B vergleichen, MP3 320 speichern', title_guide='PeakMP3 — Anleitung',
            redirect_title='PeakMP3 – Weiterleitung zur deutschen Seite', redirect_text='Weiter zur deutschen Seite'),
 'en': dict(nav='Main navigation', all='All programs', search='Search', kbd='Ctrl K', search_label='Search programs',
            theme='Switch colour scheme', legal='Legal', new='NEW', pill='Preview {v} is out',
            more="What's new →", source='Source code', terms='Terms of use',
            bento="What's inside", bento_sub='Installation, features, privacy, checks.', inst='Installation',
            inst_sub='Compare the checksum, run the setup, open PeakMP3.', terminal='Terminal',
            feat='Features', checked='Checked',
            local_title='Runs locally',
            local_text='PeakMP3 processes audio files on your PC. The listening examples on this page are prepared in advance; your files are not processed in the browser. The demo remembers only the VU calibration value you set, kept solely in your browser (localStorage) and never transmitted.',
            local_live='Local · offline',
            t_hash='Compare SHA-256 with SHA256SUMS.txt from the release', t_setup='Installs into your user profile, no administrator rights',
            t_start='Open PeakMP3 from the desktop and drop audio files',
            features=['Density 0–10', 'A/B comparison', 'Waveform & record', 'File queue', 'VU calibration', 'MP3 320', 'AAC · WAV · FLAC', 'Windows 7 SP1'],
            checks=['GitHub Actions: website build, page checks and a Windows build on every push',
                    '33 listening examples with SHA-256 checksums (music/SHA256SUMS.txt)',
                    'SHA-256 checksums for the shared installer in the release (SHA256SUMS.txt)',
                    'Music under CC BY 4.0 with attribution (music/CREDITS.md)',
                    'Windows 7 and 11 confirmed by the user; Windows 10 not tested separately'],
            installer='The installer is hosted in the YouTube Downloader release: both programs install together, and PeakMP3 has no release of its own.',
            installer_link='YouTube Downloader 2.6.0 release',
            description='Set the density, compare A/B and save MP3 320 on Windows. Analog controls, like a real unit.',
            title_home='PeakMP3 — set the density, compare A/B, save MP3 320', title_guide='PeakMP3 — User guide',
            redirect_title='PeakMP3 – redirect to the German page', redirect_text='Continue to the German page')}


def head(lang, title, description, extra_scripts=''):
    v = kit_version()
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="' + e(description) + '"><meta name="application-version" content="0.16.0">'
            '<title>' + e(title) + '</title><link rel="icon" href="assets/site/peakmp3.svg">'
            '<script src="assets/kit/kit-theme.js"></script>'
            '<link rel="stylesheet" href="assets/kit/kit.css?v=' + v + '">'
            '<link rel="preload" href="assets/site/fonts/RobotoCondensed.woff2" as="font" type="font/woff2" crossorigin>'
            '<link rel="stylesheet" href="website/site.css?v=' + SITE_REV + '"><link rel="stylesheet" href="website/peak.css?v=' + SITE_REV + '">'
            '<link rel="stylesheet" href="website/peak-kit.css?v=' + SITE_REV + '">'
            '<script src="assets/kit/programs.js?v=' + v + '" defer></script>'
            '<script src="assets/kit/kit.js?v=' + v + '" defer></script>' + extra_scripts)


def header(kind, lang):
    t = TEXT[lang]
    langs = ''.join('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (
        page_name(kind, x), x, x, ' aria-current="page"' if x == lang else '', x.upper()) for x in LANGS)
    return ('<div class="ppk-nav-wrap" id="ppk-nav-wrap">\n<nav class="ppk-nav" aria-label="%s">'
            '<a class="ppk-brand" href="%s"><img src="assets/site/peakmp3.svg" alt="" width="34" height="34"><span>PeakMP3</span></a>'
            '<span class="ppk-spacer"></span>'
            '<a class="ppk-back" href="%s">← %s</a>'
            '<button class="ppk-search-btn" type="button" data-ppk-open-search aria-label="%s"><span>%s</span><kbd>%s</kbd></button>'
            '<div class="ppk-langs">%s</div>'
            '<button class="ppk-icon-btn ppk-theme-btn" type="button" data-ppk-theme aria-label="%s"></button>'
            '<a class="ppk-icon-btn ppk-gh-btn" href="%s" aria-label="GitHub"></a>'
            '</nav>\n</div>') % (t['nav'], LANDING[lang], CATALOG[lang], t['all'], t['search_label'], t['search'], t['kbd'],
                                 langs, t['theme'], e(RELEASE['source_url']))


FOOTER_LABELS = {'ru': ('Права', 'Сообщить об ошибке'), 'de': ('Rechte', 'Problem melden'), 'en': ('Rights', 'Report a problem')}


def kit_footer(lang):
    t = TEXT[lang]
    return ('<footer class="ppk-footer">\n<span>© 2026 Anton Popov · PeakMP3 %s</span>\n'
            '<nav aria-label="%s"><a href="%simpressum.html">Impressum</a><a href="%sdatenschutz.html">Datenschutz</a>'
            '<a href="%s/blob/main/RIGHTS.md">%s</a><a href="%s">%s</a><a href="%s">GitHub</a></nav>\n</footer>') % (
        e(RELEASE['version']), t['legal'], PROFILE, PROFILE, e(RELEASE['source_url']), FOOTER_LABELS[lang][0],
        e(RELEASE['feedback_url']), FOOTER_LABELS[lang][1], e(RELEASE['source_url']))


def pill(lang):
    t = TEXT[lang]
    return ('<a class="ppk-pill" href="%s"><span class="ppk-new">%s</span><span>%s</span> <span class="ppk-more">%s</span></a>' % (
        e(RELEASE['release_url']), t['new'], e(t['pill'].format(v=RELEASE['version'])), t['more']))


def source_button(lang):
    return ('<a class="button ppk-btn ppk-btn-gh" href="%s">%s <span class="ppk-chip"><i class="ppk-dot"></i>%s</span></a>' % (
        e(RELEASE['source_url']), TEXT[lang]['source'], e(STACK)))


def installer_note(lang):
    t = TEXT[lang]
    return '<p class="installer-note">%s <a href="%s">%s</a></p>' % (e(t['installer']), e(RELEASE['release_url']), e(t['installer_link']))


def bento(lang):
    t = TEXT[lang]
    lines = [('ps', 'PS> Get-FileHash .\\' + SETUP), ('dim', t['t_hash']), ('ps', 'PS> .\\' + SETUP),
             ('dim', t['t_setup']), ('ok', t['t_start'])]
    term = ''.join('<div class="ppk-%s">%s</div>' % (c, e(x)) for c, x in lines)
    chips = ''.join('<span>%s</span>' % e(x) for x in t['features'])
    checks = ''.join('<li>%s</li>' % e(x) for x in t['checks'])
    return (
        '<section class="ppk-bento-section ppk-section ppk-reveal" aria-labelledby="bento-title">\n'
        '<h2 id="bento-title">%s</h2><p class="ppk-sub">%s</p>\n<div class="ppk-bento">\n'
        '<div class="ppk-tile ppk-wide"><h3>%s</h3><p>%s</p>'
        '<div class="ppk-term" role="group" aria-label="%s"><div class="ppk-term-bar"><i></i><i></i><i></i></div>'
        '<div class="ppk-term-out">%s</div></div></div>\n'
        '<div class="ppk-tile"><h3>%s</h3><p>%s</p><span class="ppk-live">%s</span></div>\n'
        '<div class="ppk-tile"><h3>%s</h3><div class="ppk-chips">%s</div></div>\n'
        '<div class="ppk-tile ppk-wide"><h3>%s</h3><ul class="ppk-checks">%s</ul></div>\n</div>\n</section>') % (
        t['bento'], t['bento_sub'], t['inst'], t['inst_sub'], t['terminal'], term,
        t['local_title'], e(t['local_text']), t['local_live'], t['feat'], chips, t['checked'], checks)


def redirect_page():
    """Old address of the German page: forwards to index.html and keeps the other language links."""
    t = TEXT['de']
    return ('<!doctype html>\n<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<script>location.replace(\'index.html\'+location.hash)</script><meta http-equiv="refresh" content="0; url=index.html"><link rel="canonical" href="%sPeakMP3/index.html"><meta name="robots" content="noindex">'
            '<title>%s</title></head>\n<body><p><a href="index.html">%s</a> · '
            '<a href="index-en.html" lang="en" hreflang="en">English</a> · <a href="index-ru.html" lang="ru" hreflang="ru">Русский</a></p></body></html>\n') % (
        SITE, e(t['redirect_title']), e(t['redirect_text']))
