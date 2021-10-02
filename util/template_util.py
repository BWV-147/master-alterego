import os

from PIL import Image
from matplotlib import pyplot as plt

from util.autogui import screenshot
from util.base import *
from util.config import config

base_path: Optional[str] = None


def show_img(img, name=None):
    fig = plt.figure(name, figsize=(6.4, 6.4 * 1080 / 1920), facecolor='red', clear=True)
    fig.add_axes([0, 0, 1, 1])
    plt.axis('off')
    plt.imshow(img, aspect='auto', interpolation='nearest')
    plt.show()


def capture(fn: str = None, _base: str = None):
    # pyautogui.hotkey('alt', 'tab')
    _base = _base or base_path
    if _base and not os.path.exists(_base):
        os.makedirs(_base)
        print(f'make dir: {_base}')
    time.sleep(0.1)
    t0 = time.time()
    img = screenshot()
    if fn and _base is not None:
        full_fp = os.path.join(_base or base_path, fn + '.png')
        if os.path.exists(full_fp):
            print(f'! Replace: "{full_fp}"', end='')
        else:
            print(f'   Save  : "{full_fp}" saved', end='')
        print(f'\t\t{time.time() - t0:.4f} sec')
        img.save(full_fp)
    show_img(img, 'screenshot')
    # pyautogui.hotkey('alt', 'tab')


def save_rewards(quest_name: str = None, cfg=None, count=True, drop: int = None):
    config.load(cfg)
    img = screenshot()
    if quest_name:
        if count:
            config.count_battle()
        fn = f'img/_drops/{quest_name}/rewards-{quest_name}-{time.strftime("%m%d-%H%M")}-{config.battle.finished}'
        if drop:
            fn += f'-drop{drop}'
            config.record_craft_drop()
        fn += '.png'
        print(f'Save "{fn}"')
        img.save(fn)
        config.save()
    show_img(img, 'rewards')


def compare(m1: Union[str, Image.Image], m2: Union[str, Image.Image], region, dx=0, dy=0, dw=0, dh=0):
    plt.figure('compare', clear=True)
    if isinstance(m1, str):
        m1 = Image.open(m1)
    if isinstance(m2, str):
        m2 = Image.open(m2)
    plt.subplot(1, 2, 1)
    plt.imshow(m1.crop(region))
    plt.subplot(1, 2, 2)
    region2 = [region[0] + dx, region[1] + dy, region[2] + dx + dw, region[3] + dy + dh]
    plt.imshow(m2.crop(region2))
    print(f'{region}\n{tuple(region2)}')
    plt.show()
