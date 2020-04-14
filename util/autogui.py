"""Image related processing"""
import traceback

import cv2
import numpy
from PIL import ImageGrab
from scipy.signal import find_peaks
from skimage.feature import match_template as sk_match_template
from skimage.metrics import structural_similarity as sk_compare_ssim

from util.dataset import *
from util.gui import *


def screenshot(region: Sequence = None, filepath: str = None, monitor: int = None) -> Image.Image:
    """
    take screenshot of multi-monitors. set python.exe and pythonw.exe high dpi first!(see README.md)

    :param region: region inside monitor
    :param filepath: if not None, save to `filepath` then return
    :param monitor: 0-total size of all monitors, 1-main, 2-second monitor
    :return: PIL.Image.Image
    """
    if monitor is None:
        monitor = config.monitor
    _image = None
    size = (1920, 1080)
    try:
        with mss() as sct:
            mon = sct.monitors[monitor]
            size = (mon['width'], mon['height'])
            shot = sct.grab(mon)
            _image = Image.frombytes('RGB', size, shot.rgb).crop(region)
    except Exception as e:
        logger.error(f'Fail to grab screenshot using mss(). Error:\n{e}', NO_LOG_TIME)
        if config.monitor == 1 and tuple(config.offset) == (0, 0):
            # ImageGrab can only grab the main screen
            try:
                _image = ImageGrab.grab()
            except Exception as e:
                logger.error(f'Fail to grab screenshot using ImageGrad. Error:\n{e}', NO_LOG_TIME)
        logger.error(traceback.format_exc(), NO_LOG_TIME)
    if _image is None:
        # grab failed, return a empty image with single color
        _image = Image.new('RGB', size, (0, 255, 255)).crop(region)
    if filepath is not None:
        _image.save(filepath)
    return _image


def get_mean_color(img: Image.Image, region: Sequence):
    if len(region) == 2:
        return img.getpixel(region)
    elif len(region) == 4:
        return numpy.mean(list(img.crop(region).getdata()), 0)
    else:
        raise KeyError(f'len(region) != 2 or 4. region={region}')


def cal_sim(img1: Image.Image, img2: Image.Image, region=None, method='ssim') -> float:
    """
    Calculate the similarity of two image at region.

    :param img1:
    :param img2:
    :param region: region to crop.
    :param method: 'ssim': compute the mean structural similarity using `skimage`.
                   'hist': compute the similarity of color histogram
    :return: similarity, float between (0,1).
    """
    if region is not None:
        img1 = img1.crop(region)
        img2 = img2.crop(region)
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    if method == 'ssim':
        # noinspection PyTypeChecker
        sim = sk_compare_ssim(numpy.array(img1), numpy.array(img2), multichannel=True)
    elif method == 'hist':
        size = tuple(numpy.min((img1.size, img2.size), 0))
        if size != img1.size:
            img1 = img1.resize(size)
            img2 = img2.resize(size)
        lh = img1.histogram()
        rh = img2.histogram()

        sim = sum(1 - (0 if _l == _r else float(abs(_l - _r)) / max(_l, _r)) for _l, _r in zip(lh, rh)) / len(lh)
    else:
        raise ValueError(f'invalid method "{method}", only "ssim" and "hist" supported')
    # print(f'sim={sim:.4f}   \r', end='')
    return sim


def _fix_length(images: Union[Image.Image, Sequence[Image.Image]], regions: Sequence):
    # fix to equal length of images and regions
    if isinstance(images, Image.Image):
        images = [images]
    images = list(images)
    if regions is None:
        regions = [None] * len(images)
    elif isinstance(regions[0], (int, float)):
        regions = [regions] * len(images)
    else:
        if len(images) == len(regions):
            pass
        elif len(images) == 1:
            images = list(images) * len(regions)
        elif len(regions) == 1:
            regions = list(regions) * len(images)
        else:
            assert False, f'lengths should be equal or 1:\n {(images, regions)}'
    return images, regions


def match_one_target(img: Image.Image, target: Image.Image, region: Sequence, threshold: float = THR) -> bool:
    return cal_sim(img, target, region) >= threshold


def match_targets(img, targets, regions=None, threshold=THR, at=None, lapse=0.0):
    # type:(Image.Image,Union[Image.Image,Sequence[Image.Image]],Sequence,float,Union[int,Sequence],float)->bool
    """
    Match all targets. See `wait_targets`.
    `at` is a region or an **int** value of target index.

    :return: bool, matched or not.
    """
    targets, regions = _fix_length(targets, regions)
    for target, region in zip(targets, regions):
        if cal_sim(img, target, region) < threshold:
            return False
    if at is None:
        pass
    elif isinstance(at, Sequence):
        click(at, lapse)
    elif at is not True and isinstance(at, int) and 0 <= at < len(regions):
        # add first condition since isinstance(True, int)=True
        click(regions[at], lapse)
    else:
        assert False, f'*at* should be int or a region: at={at}'
    return True


# 匹配第几个target
def match_which_target(img, targets, regions=None, threshold=THR, at=None, lapse=0.0):
    # type:(Image.Image,Union[Image.Image,Sequence[Image.Image]],Sequence,float,Union[bool,Sequence],float)->int
    """
    Compare targets to find which matches. See `wait_which_target`.
    `at` is a region or **bool** value `True`, if True, click matched region.

    :return: matched index, return -1 if not matched.
    """
    targets, regions = _fix_length(targets, regions)
    assert len(targets) > 1, f'length of targets or regions must be at least 2: {(len(targets), len(regions))}'
    res = -1
    for target, region in zip(targets, regions):
        res += 1
        if cal_sim(img, target, region) >= threshold:
            if at is None:
                pass
            elif isinstance(at, Sequence):
                click(at, lapse)
            elif at is True:
                click(regions[res], lapse)
            else:
                assert False, f'*at* should be True or a region: at={at}'
            return res
    return -1


def wait_targets(targets, regions, threshold=THR, at=None, lapse=0.0, clicking=None, interval=0.2):
    # type:(Union[Image.Image,Sequence[Image.Image]],Union[int,Sequence],float,Union[int,Sequence],float,Sequence,float)->None
    """
    Waiting screenshot to match all targets.

    :param : See `wait_which_target`
    :return: None
    """
    n = 0
    while True:
        n += 1
        if match_targets(screenshot(), targets, regions, threshold, at, lapse):
            print(f'in wait_regions: n={n}')
            return
        if clicking is not None:
            click(clicking, 0)
        time.sleep(interval)


# 直到匹配某一个target
def wait_which_target(targets, regions, threshold=THR, at=None, lapse=0.0, clicking=None, interval=0.2):
    # type:(Union[Image.Image,Sequence[Image.Image]],Sequence,float,Union[bool,Sequence],float,Sequence,float)->int
    """
    Waiting for screenshot to match one of targets.

    :param targets: one Image or list of Image.
    :param regions: one region or list of region.
            `targets` or `regions` must contains at least 2 elements.
            length of targets and regions could be (1,n), (n,1), (n,n), where n>=2.
    :param threshold:
    :param at:  if True, click the region which target matches,
            if a region, click the region.
    :param lapse: lapse when click `at`.
    :param clicking: a region to click at until screenshot matches some target.
            e.g. Arash death animation, kizuna->rewards page.
    :param interval: interval of loop when no one matched.
    :return: the index which target matches.
    """
    while True:
        res = match_which_target(screenshot(), targets, regions, threshold, at, lapse)
        if res >= 0:
            return res
        if clicking is not None:
            click(clicking, 0)
        time.sleep(interval)


# 直到匹配模板
def wait_search_template(target: Image.Image, threshold=THR, lapse=0.0, interval=0.2):
    while True:
        if search_target(screenshot(), target)[0] >= threshold:
            time.sleep(lapse)
            return
        time.sleep(interval)


# 搜索目标模板存在匹配的最大值
# noinspection PyTypeChecker
def search_target(img: Image.Image, target: Image.Image, mode='cv2'):
    """
    find the max matched target in img.

    :param img:
    :param target:
    :parameter mode: 'cv2'(default) to use open-cv(quick), 'sk' to use skimage package(VERY slow)
            Attention: cv2 use (h,w), but PIL/numpy use (w,h).
    :return (max value, left-top pos)
    """
    m1: numpy.ndarray = numpy.array(img.convert('RGB'))
    m2: numpy.ndarray = numpy.array(target.convert('RGB'))
    if mode == 'sk':
        matches: numpy.ndarray = sk_match_template(m1, m2)
        max_match = numpy.max(matches)
        pos = numpy.where(matches == max_match)
        return numpy.max(matches), (pos[1][0], pos[0][0])
    else:
        cv_img, cv_target = (cv2.cvtColor(m1, cv2.COLOR_RGB2BGR), cv2.cvtColor(m2, cv2.COLOR_RGB2BGR))
        # h, w = cv_target.shape[0:2]
        matches = cv2.matchTemplate(cv_img, cv_target, cv2.TM_CCOEFF_NORMED)
        max_match = numpy.max(matches)
        pos = numpy.where(matches == max_match)
        # in PIL system, (x~w,y~h)
        return numpy.max(matches), (pos[1][0], pos[0][0])


# noinspection PyTypeChecker
def search_peaks(image: Image.Image, target: Image.Image, column=True, threshold=THR, **kwargs) -> numpy.ndarray:
    """
    Find target position in img which contains several targets. For simplicity, `target` and `image` should have
    the same width or height. Thus it's 1-D search.

    :param image:
    :param target:
    :param column: search target in column or in row direction.
    :param threshold:
    :param kwargs: extra args for `scipy.signal.find_peaks`
    :return: offsets of peaks in column/row direction.
    """
    if column is True:
        assert image.size[0] == target.size[0], f'must be same width: img {image.size}, target {target.size}.'
    else:
        assert image.size[1] == target.size[1], f'must be same height: img {image.size}, target {target.size}.'
    m1: numpy.ndarray = numpy.array(image.convert('RGB'))
    m2: numpy.ndarray = numpy.array(target.convert('RGB'))
    cv_img, cv_target = (cv2.cvtColor(m1, cv2.COLOR_RGB2BGR), cv2.cvtColor(m2, cv2.COLOR_RGB2BGR))
    matches: numpy.ndarray = cv2.matchTemplate(cv_img, cv_target, cv2.TM_CCOEFF_NORMED)
    return find_peaks(matches.reshape(matches.size), height=threshold, **kwargs)[0]
