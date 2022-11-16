# rdp-manipulations

Tool for image-based control RDP (Remote Desktop Protocol). Manipulations, automations and testing via Python and Apache Guacamole

## Prerequisites

Installed and configured [Apache Guacamole](https://guacamole.apache.org/). I used this guacamole docker project: https://github.com/boschkundendienst/guacamole-docker-compose

## Examples

see `./examples` folder. To run it, clone this repo, and:

```
poetry shell
poetry install
python examples/copy_and_zip.py
```

## Supported OS

Only Windows 7 is currently supported because I only needed to work with Windows 7 PCs. If you need support for other OSes, use your [`ASSERT_DICT`](#main.ASSERT_DICT), make a pull request, or write an issue. We'll figure something out.

# Table of Contents

- [main](#main)
  - [ASSERT_DICT](#main.ASSERT_DICT)
  - [RDP](#main.RDP)
    - [\_\_init\_\_](#main.RDP.__init__)
    - [login](#main.RDP.login)
    - [key_press](#main.RDP.key_press)
    - [key_type](#main.RDP.key_type)
    - [make_screenshot](#main.RDP.make_screenshot)
    - [is_on_screen](#main.RDP.is_on_screen)
    - [wait_until_appear](#main.RDP.wait_until_appear)
    - [wait_until_desappear](#main.RDP.wait_until_desappear)
    - [exec_remote](#main.RDP.exec_remote)
    - [copydir](#main.RDP.copydir)
    - [copy](#main.RDP.copy)
    - [mkdir](#main.RDP.mkdir)
    - [opendir](#main.RDP.opendir)
    - [closedir](#main.RDP.closedir)
    - [mouse_click](#main.RDP.mouse_click)
    - [mouse_move](#main.RDP.mouse_move)
    - [mouse_move_to](#main.RDP.mouse_move_to)
    - [mouse_click_to](#main.RDP.mouse_click_to)
    - [current_lang](#main.RDP.current_lang)
    - [lang_switch](#main.RDP.lang_switch)
    - [logout](#main.RDP.logout)

<a id="main"></a>

# main

<a id="main.ASSERT_DICT"></a>

#### ASSERT_DICT

Pass it to instance of [`RDP`](#main.RDP) for unsupported OS (see below)

```
{
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
```

<a id="main.RDP"></a>

## RDP Objects

```python
class RDP()
```

RDP class

<a id="main.RDP.__init__"></a>

#### \_\_init\_\_

```python
def __init__(headless=headless,
             width=width,
             height=height,
             clear_logs=clear_logs,
             assert_dict=ASSERT_DICT) -> None
```

**Arguments**:

- `headless` _bool, optional_ - if False rdp window is shown.
  (default is True)
- `width` _int, optional_ - witdth of rdp window. Set it same in guacamole
  (default is 800)
- `height` _int, optional_ - witdth of rdp window. Set it same in guacamole
  (default is 600)
- `clear_logs` _bool, optional_ - if True old image logs will be removed when RDP class inited.
  (default is True)
- `assert_dict` _dict, optional_ - dict with assertion images. Pass it for unsupported OS
  (default is [`ASSERT_DICT`](#main.ASSERT_DICT))

<a id="main.RDP.login"></a>

#### login

```python
def login(guacamole_user: str,
          guacamole_password: str,
          guacamole_pc_name: str,
          guacamole_url=guacamole_url) -> None
```

Login method. Call this first

<a id="main.RDP.key_press"></a>

#### key_press

```python
def key_press(keys: str)
```

This is wrapper of playwright keyboard.press method. see: https://playwright.dev/python/docs/api/class-keyboard#keyboard-press

<a id="main.RDP.key_type"></a>

#### key_type

```python
def key_type(text: str)
```

Type text on remote pc

<a id="main.RDP.make_screenshot"></a>

#### make_screenshot

```python
def make_screenshot(filename: Optional[str] = None,
                    path: Optional[str] = None) -> str
```

Make screenshot, and save it to default direcotry (./image_logs), or to given path

<a id="main.RDP.is_on_screen"></a>

#### is_on_screen

```python
def is_on_screen(assertion: str, threshold: float = image_threshold) -> bool
```

Checking assertion image is on screen (assertion is a path to image)

<a id="main.RDP.wait_until_appear"></a>

#### wait_until_appear

```python
def wait_until_appear(assertion: str,
                      attempts: int = screen_state_attempts,
                      threshold: float = image_threshold) -> None
```

Waiting until assertion image is appear on screen (assertion is a path to image)

<a id="main.RDP.wait_until_desappear"></a>

#### wait_until_desappear

```python
def wait_until_desappear(assertion: str,
                         attempts: int = screen_state_attempts,
                         threshold: float = image_threshold) -> None
```

Waiting until assertion image is desappear on screen (assertion is a path to image)

<a id="main.RDP.exec_remote"></a>

#### exec_remote

```python
def exec_remote(cmd_str: str) -> None
```

Execute remote command via win+r run window

<a id="main.RDP.copydir"></a>

#### copydir

```python
def copydir(from_path: str, to_path: str) -> None
```

Copy folder on remote PC

<a id="main.RDP.copy"></a>

#### copy

```python
def copy(from_path: str, to_path: str) -> None
```

Copy file on remote PC

<a id="main.RDP.mkdir"></a>

#### mkdir

```python
def mkdir(dir_path: str) -> None
```

Making directory

<a id="main.RDP.opendir"></a>

#### opendir

```python
def opendir(dir_path: str, local: bool = False) -> None
```

Open explorer.exe of given directory path

<a id="main.RDP.closedir"></a>

#### closedir

```python
def closedir(dir_name: str) -> None
```

Close explorer.exe of given directory name

<a id="main.RDP.mouse_click"></a>

#### mouse_click

```python
def mouse_click(x: float, y: float, click_count: int = 1) -> None
```

Mouse left click on remote PC by giving coordinates

<a id="main.RDP.mouse_move"></a>

#### mouse_move

```python
def mouse_move(x: float, y: float) -> None
```

Mouse move on remote PC by giving coordinates

<a id="main.RDP.mouse_move_to"></a>

#### mouse_move_to

```python
def mouse_move_to(assertion: str) -> Optional[tuple[float, float]]
```

Mouse move on remote PC by giving image assertion path

<a id="main.RDP.mouse_click_to"></a>

#### mouse_click_to

```python
def mouse_click_to(
        assertion: str,
        button: Literal['left', 'middle', 'right'] = 'left') -> None
```

Mouse click on remote PC by giving image assertion path

<a id="main.RDP.current_lang"></a>

#### current_lang

```python
def current_lang() -> Optional[str]
```

Get a current keuboard language (now support only 'en' and 'ru')

<a id="main.RDP.lang_switch"></a>

#### lang_switch

```python
def lang_switch(lang: Optional[str] = None) -> Optional[str]
```

Switch keuboard language (now support only 'en' and 'ru')

<a id="main.RDP.logout"></a>

#### logout

```python
def logout() -> None
```

Logout method
