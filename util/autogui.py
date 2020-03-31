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
    calculate the similarity of two image at region.
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


# 是否匹配一个或多个regions
def compare_regions(img, target, regions=None, threshold=THR, at=None):
    # type:(Image.Image,Image.Image,Sequence,float,Union[bool,Sequence])->bool
    """
    compare two image at `region`, click `at` if matches. use `screenshot()` as img if img is None
    :return: bool: match or not
    """
    if regions is None:
        res = cal_sim(img, target) > threshold
    else:
        if isinstance(regions[0], Sequence):
            matches = [cal_sim(img.crop(region), target.crop(region)) > threshold for region in regions]
            res = False not in matches
        else:
            res = cal_sim(img.crop(regions), target.crop(regions)) > threshold
    if res:
        if at is True:
            click(regions)
        elif isinstance(at, Sequence):
            click(at)
    return res


# 匹配第几个target
def match_which_target(img, targets, regions=None, threshold=THR, at=None):
    # type:(Image.Image,Union[Image.Image,Sequence[Image.Image]],Sequence,float,Union[bool,Sequence])->int
    """
    compare img with multi targets, click `at` if matches.
    :return: matched index, -1 if not matched.
    """
    if isinstance(targets, Image.Image):
        targets = [targets]
    if regions is None:
        regions = [None for _ in targets]
    if isinstance(regions[0], (int, float)):
        regions = [regions]
    assert len(targets) == len(regions), (targets, regions)
    res = -1
    for i in range(len(targets)):
        sim = cal_sim(img, targets[i], regions[i])
        if config.temp.get('print_sim') is True:
            print(f'sim={sim}')
        if sim > threshold:
            res = i
            break
    if res >= 0:
        if at is True:
            click(regions[res])
        elif isinstance(at, Sequence):
            click(at)
    return res


def is_match_target(img, target, region=None, threshold=THR, at=None):
    # type:(Image.Image,Image.Image,Sequence,float,Union[bool,Sequence])->bool
    return match_which_target(img, target, region, threshold, at) >= 0


# 直到匹配某一个target
def wait_which_target(targets, regions, threshold=THR, lapse=0.1, at=None, clicking=None, interval=0.5):
    # type:(Union[Image.Image,Sequence[Image.Image]],Sequence,float,float,Union[bool,Sequence],Sequence,int)->int
    """
    Waiting for screenshot matching the region of some target.
    :param targets: an Image or list of Image.
    :param regions: corresponding region to target.
    :param threshold:
    :param lapse:
    :param at:  if True, click the region which screenshot matches,
                if a region, click the region `at`.
    :param clicking: a region to click at until screenshot matches some target
    :param interval: interval of clicking loop
    :return: the index which target matches.
    """
    if isinstance(targets, Image.Image):
        targets = [targets]
        regions = [regions]
    num = len(targets)
    assert len(regions) == num, (targets, regions)

    while True:
        shot = screenshot()
        res = match_which_target(shot, targets, regions, threshold, at)
        if res >= 0:
            time.sleep(lapse)
            return res
        if clicking is not None:
            click(clicking, lapse=interval)


def wait_targets(target, regions, threshold=THR, lapse=0.1, at=None, clicking=None, interval=0.5):
    if not isinstance(regions[0], Sequence):
        regions = [regions]
    while True:
        shot = screenshot()
        res = [is_match_target(shot, target, region, threshold) for region in regions]
        if False not in res:
            break
        if clicking is not None:
            click(clicking, lapse=interval)
    if at is True and len(regions) == 1:
        click(regions[0])
    elif isinstance(at, Sequence):
        click(at)
    time.sleep(lapse)


# 直到匹配模板
def wait_search_template(target: Image.Image, threshold=THR, lapse=0.1):
    while True:
        if search_target(screenshot(), target)[0] > threshold:
            return
        time.sleep(lapse)


# 搜索目标模板存在匹配的最大值
# noinspection PyTypeChecker,PyUnresolvedReferences
def search_target(img: Image.Image, target: Image.Image, mode='cv2'):
    """
    return the maximum of matched
    mode ='cv2'(default) to use open-cv(quick), 'sk' to use skimage package(VERY slow)
    Attention: cv2 use (h,w), but PIL/numpy use (w,h).
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


# noinspection PyTypeChecker,PyUnresolvedReferences
def search_peaks(img: Image.Image, target: Image.Image, column=True, threshold=THR, **kwargs):
    if column is True:
        assert img.size[0] == target.size[0], f'must be same width: img {img.size}, target {target.size}.'
    else:
        assert img.size[1] == target.size[1], f'must be same height: img {img.size}, target {target.size}.'
    m1: numpy.ndarray = numpy.array(img.convert('RGB'))
    m2: numpy.ndarray = numpy.array(target.convert('RGB'))
    cv_img, cv_target = (cv2.cvtColor(m1, cv2.COLOR_RGB2BGR), cv2.cvtColor(m2, cv2.COLOR_RGB2BGR))
    matches: numpy.ndarray = cv2.matchTemplate(cv_img, cv_target, cv2.TM_CCOEFF_NORMED)
    return find_peaks(matches.reshape(matches.size), height=threshold, **kwargs)[0]
