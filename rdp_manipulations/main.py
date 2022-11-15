import re
from pathlib import Path
from playwright.sync_api import sync_playwright, Playwright, Browser, Page
from typing import Optional, Literal

from rdp_manipulations.logger import logger
from image_processing.main import is_image_contain, is_image_identic, image_locate_center

LANG_SWITCH_KEYS = 'Alt+Shift'

CMD_DICT = {
    'mkdir': 'cmd.exe /c mkdir {dir_path}',
    'opendir': 'explorer.exe "{dir_path}"',
    'copy': 'cmd.exe /c xcopy "{from_path}" ' + '"{to_path}" /e /i',
    'closedir': 'cmd.exe /c taskkill /im explorer.exe /fi "windowtitle eq {dir_name}"'
}

ASSERT_DICT = {
    'prelogin': './image_asserts/prelogin.png',
    'login': './image_asserts/login.png',
    'post_login': './image_asserts/post_login.png',
    'start_btn': './image_asserts/start_btn.png',
    'start_btn_selected': './image_asserts/start_btn_selected.png',
    'run_window': './image_asserts/run_window.png',
    'lang_ru': './image_asserts/lang_ru.png',
    'lang_en': './image_asserts/lang_en.png',
    'opened_folder': './image_asserts/opened_folder.png',
    'files_copy': './image_asserts/files_copy.png',
}


def get_key_by_value(_dict: dict[str, str], value: str) -> str:
    p = dict(zip(_dict.values(), _dict.keys()))
    try:
        return p[value]
    except:
        return value


def has_cyrillic(text: str):
    # TODO Ускорить набор текста добавивь спецсимволы типа слешей и точек
    return bool(re.search('[а-яА-Я]', text))


class RDP:
    headless: bool = False
    width: int = 800
    height: int = 600
    playwright: Playwright
    browser: Browser
    page: Page
    screen_state_attempts: int = 10
    screen_state_delay: int = 3000
    keyboard_delay: int = 100
    ui_delay: int = 500
    mouse_steps: int = 10
    image_threshold: float = 0.8
    guacamole_url: str = 'http://localhost:8080/guacamole/#/'
    image_logs_path: str = './image_logs/'
    clear_logs: bool = True

    def __init__(self, headless=headless, width=width, height=height, clear_logs=clear_logs) -> None:
        self.screenshot_counter = 0
        self.lang: Optional[str] = None
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
            viewport={"width": width, "height": height})
        self.context.grant_permissions(['clipboard-read', 'clipboard-write'])
        self.page = self.context.new_page()
        if clear_logs:
            self.__clear_logs()

    def __clear_logs(self):
        for f in Path(self.image_logs_path).glob("*.png"):
            if f.is_file():
                f.unlink()

    def __wait_until_screen_state(self, assertion: str, will_appear: bool = True, attempts: int = screen_state_attempts, threshold: float = image_threshold) -> bool:
        if will_appear:
            msg = '💤 Waiting for "{}" is appear on screen. Attempts left: {}'
        else:
            msg = '💤 Waiting for "{}" is desappear from screen. Attempts left: {}'
        assertion_text = get_key_by_value(ASSERT_DICT, assertion)
        msg_text = msg.format(assertion_text, attempts)
        logger.debug(msg_text)

        result = self.is_on_screen(assertion, threshold=threshold)
        print('result', result)
        if result is not will_appear and attempts:
            self.delay(self.screen_state_delay)
            return self.__wait_until_screen_state(assertion, will_appear=will_appear, attempts=attempts-1, threshold=threshold)
        else:
            if result is not will_appear:
                logger.critical(msg_text)
                raise RuntimeError(msg_text)
            return result is will_appear

    def delay(self, delay: int = ui_delay) -> None:
        return self.page.wait_for_timeout(delay)

    def key_press(self, keys: str):
        self.delay()
        self.page.keyboard.press(keys, delay=self.keyboard_delay)
        self.delay()

    def key_type(self, text: str):
        self.lang = self.current_lang()
        self.delay()
        for char in text:
            logger.debug(
                f'Current lang is: {self.lang}, and char "{char}" is_cyrillic == {has_cyrillic(char)}')
            if self.lang == 'en' and has_cyrillic(char):
                logger.debug('will self.lang_switch ru')
                self.lang_switch('ru')
            if self.lang == 'ru' and not has_cyrillic(char):
                logger.debug('will self.lang_switch en')
                self.lang_switch('en')
            self.page.keyboard.type(char, delay=self.keyboard_delay)

    def make_screenshot(self, filename: Optional[str] = None, path: Optional[str] = None) -> str:
        if path:
            sc_path = path
        elif filename:
            sc_path = f'{self.image_logs_path}/{filename}.png'
        else:
            sc_path = f'{self.image_logs_path}/screenshot_{self.screenshot_counter}.png'
        self.screenshot_counter += 1
        self.page.screenshot(path=sc_path)
        logger.debug(f'screenshot saved: {sc_path}')
        return sc_path

    def is_on_screen(self, assertion: str, threshold: float = image_threshold) -> bool:
        return is_image_identic(assertion, self.make_screenshot(), threshold=threshold) or is_image_contain(assertion, self.make_screenshot(), threshold=threshold)

    def wait_until_appear(self, assertion: str, attempts: int = screen_state_attempts, threshold: float = image_threshold) -> None:
        self.delay()
        self.__wait_until_screen_state(assertion, will_appear=True, attempts=attempts, threshold=threshold)
        self.delay()

    def wait_until_desappear(self, assertion: str, attempts: int = screen_state_attempts, threshold: float = image_threshold) -> None:
        self.delay()
        self.__wait_until_screen_state(assertion, will_appear=False, attempts=attempts, threshold=threshold)
        self.delay()

    def exec_remote(self, cmd_str: str) -> None:
        logger.debug(f'Remote exec: {cmd_str}')
        self.key_press("Meta+KeyR")
        self.key_press("Backspace")
        self.wait_until_appear(ASSERT_DICT['run_window'], threshold=0.24)
        self.key_type(cmd_str)
        self.make_screenshot('cmd_str')
        self.key_press("Enter")
        self.wait_until_desappear(ASSERT_DICT['run_window'], threshold=0.24)
        self.delay()

    def copy(self, from_path: str, to_path: str) -> None:
        logger.info(f'Copying {from_path} to {to_path} 💾')
        cmd_str = CMD_DICT['copy'].format(from_path=from_path, to_path=to_path)
        self.exec_remote(cmd_str)
        self.wait_until_desappear(ASSERT_DICT['files_copy'])
        logger.success('Folder copied successfully 💾')

    def mkdir(self, dir_path: str) -> None:
        logger.info(f'Making directory {dir_path}')
        cmd_str = CMD_DICT['mkdir'].format(dir_path=dir_path)
        self.exec_remote(cmd_str)
        logger.success('Done')

    def opendir(self, dir_path: str, local: bool = False) -> None:
        logger.info(f'Opening directory {dir_path}')
        cmd_name = 'opendir_local' if local else 'opendir'
        if local:
            # FIXME понять как определить что диск готов. Сейчас тупо таймер с запасом
            logger.info('Waiting for netdisk will mount. FIXME')
            self.delay(10000)
        cmd_str = CMD_DICT[cmd_name].format(dir_path=dir_path)
        self.exec_remote(cmd_str)
        self.wait_until_appear(ASSERT_DICT['opened_folder'])
        self.delay(5000)
        logger.success('Opening directory done !')

    def mouse_click(self, x: float, y: float, click_count: int = 1) -> None:
        self.delay()
        self.page.mouse.click(x, y, click_count=click_count,
                              delay=self.keyboard_delay)
        self.delay()

    def mouse_move(self, x: float, y: float) -> None:
        self.delay()
        self.page.mouse.move(0, 0, steps=10)
        logger.debug(f'Move mouse to {x} {y}')
        self.page.mouse.move(x, y, steps=self.mouse_steps)
        self.delay()

    def mouse_move_to(self, assertion: str) -> Optional[tuple[float, float]]:
        self.delay()
        result = image_locate_center(assertion, self.make_screenshot())
        logger.debug(f'assertion found {assertion} at {result}')
        if result:
            self.mouse_move(*result)
            self.delay()
            return result
        return None

    def mouse_click_to(self, assertion: str, button: Literal['left', 'middle', 'right'] = 'left') -> None:
        result = self.mouse_move_to(assertion)
        if result:
            self.page.mouse.down(button=button)
            self.delay()
            self.page.mouse.up(button=button)
            self.delay()
            logger.debug('Mouse {button} clicked')

    def closedir(self, dir_name: str) -> None:
        logger.info('Closing directory {dir_name}')
        cmd_str = CMD_DICT['closedir'].format(dir_name=dir_name)
        self.exec_remote(cmd_str)
        self.wait_until_desappear(ASSERT_DICT['opened_folder'])
        self.make_screenshot('closed_folder')
        logger.success('Closing directory done')

    def current_lang(self) -> Optional[str]:
        if self.is_on_screen(ASSERT_DICT['lang_ru']):
            return 'ru'
        if self.is_on_screen(ASSERT_DICT['lang_en']):
            return 'en'
        return None

    def lang_switch(self, lang: Optional[str] = None) -> Optional[str]:
        self.key_press(LANG_SWITCH_KEYS)
        self.page.wait_for_timeout(2000)
        self.lang = self.current_lang()
        if self.lang != lang:
            return self.lang_switch(lang)
        return self.lang

    def login(self, guacamole_user: str, guacamole_password: str, guacamole_pc_name: str, guacamole_url=guacamole_url) -> None:
        logger.info('👨‍💻 Attempt to login via RDP')
        self.page.goto(guacamole_url)
        self.page.get_by_label("Username").fill(guacamole_user)
        self.page.get_by_label("Password").fill(guacamole_password)
        self.page.get_by_role("button", name="Login").click()
        link = self.page.get_by_role("link", name=guacamole_pc_name)
        href = str(link.get_attribute("href"))
        link.click()
        self.page.wait_for_url(href, wait_until="networkidle")
        self.page.wait_for_load_state("networkidle")
        self.make_screenshot('prelogin')
        self.wait_until_desappear(ASSERT_DICT['prelogin'], threshold=0.99)
        self.make_screenshot('login')
        self.wait_until_desappear(ASSERT_DICT['login'])
        self.key_press('Escape')  # Чтобы убрать фокус с кнопки пуск (не всегда работает)
        try:
            self.wait_until_appear(ASSERT_DICT['start_btn'], threshold=0.5)  # HACK: низкий порог чтобы работало с разными языками
        except RuntimeError:
            self.wait_until_appear(ASSERT_DICT['start_btn_selected'], threshold=0.5)
        self.make_screenshot('after_login')
        logger.success('👨‍💻 RDP login successful!')

    def logout(self) -> None:
        # TODO: сделать разлогинивание
        self.context.close()
        self.browser.close()
