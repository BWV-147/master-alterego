"""Image processing and computation"""
import numpy as np
from PIL import ImageGrab
import cv2
from mss import mss
from skimage.measure import compare_ssim as sk_compare_ssim
from skimage.feature import match_template as sk_match_template
from util.dataset import *


def screenshot(region: Union[tuple, list] = None, filepath: str = None, monitor=1) -> Image.Image:
    """
    take screenshot of multi-monitors. set python.exe and pythonw.exe high dpi first!(see README.md)
    :param region: region inside monitor
    :param filepath:
    :param monitor: 0-all monitor, 1-first, 2-second monitor
    :return: PIL.Image.Image
    """
    try:
        with mss() as sct:
            mon = sct.monitors[monitor]
            shot = sct.grab(mon)
            _image = Image.frombytes('RGB', (mon['width'], mon['height']), shot.rgb).crop(region)
    except Exception as e:
        logger.error('grab screenshot failed, return default single color image.\n%s' % e)
        _image = Image.new('RGB', (1920, 1080), (0, 255, 255)).crop(region)
    if filepath is not None:
        _image.save(filepath)
    return _image


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
        sim = sk_compare_ssim(np.array(img1), np.array(img2), multichannel=True)
    elif method == 'hist':
        size = tuple(np.min((img1.size, img2.size), 0))
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
    # type:(Image.Image,Image.Image,Union[tuple,list],float,Union[bool,tuple,list])->bool
    """
    compare two image at `region`, click `at` if matches. use `screenshot()` as img if img is None
    :return: bool: match or not
    """
    if regions is None:
        res = cal_sim(img, target) > threshold
    else:
        if isinstance(regions[0], (list, tuple)):
            matches = [cal_sim(img.crop(region), target.crop(region)) > threshold for region in regions]
            res = False not in matches
        else:
            res = cal_sim(img.crop(regions), target.crop(regions)) > threshold
    # if isinstance(regions, (list, tuple)):
    #     if isinstance(regions[0], (list, tuple)):
    #         matches = [cal_sim(img.crop(region), target.crop(region)) > threshold for region in regions]
    #         res = matches.count(True) == len(regions)
    #     else:
    #         res = cal_sim(img.crop(regions), target.crop(regions)) > threshold
    # else:
    #     res = cal_sim(img.crop(regions), target.crop(regions)) > threshold
    if res:
        if at is True:
            click(regions)
        elif isinstance(at, (tuple, list)):
            click(at)
    return res


# 匹配第几个target
def match_which_target(img, targets, regions, threshold=THR, at=None):
    # type:(Image.Image,Union[Image.Image,tuple,list],Union[list,tuple],float,Union[bool,tuple,list])->int
    """
    compare img with multi targets, click `at` if matches.
    :return: matched index, -1 if not matched.
    """
    if isinstance(targets, Image.Image):
        targets = [targets]
    if isinstance(regions[0], (int, float)):
        regions = [regions]
    assert len(targets) == len(regions), (targets, regions)
    res = -1
    for i in range(len(targets)):
        sim = cal_sim(img, targets[i], regions[i])
        if sim > threshold:
            res = i
            break
    if res >= 0:
        if at is True:
            click(regions[res])
        elif isinstance(at, (tuple, list)):
            click(at)
    return res


# 直到匹配某一个target
def wait_which_target(targets, regions, threshold=THR, lapse=0.1, at=None, clicking=None, interval=0.5):
    # type:(Union[Image.Image,tuple,list],Union[list,tuple],float,float,Union[bool,tuple,list],Union[list,tuple],int)->int
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
            return res
        if clicking is not None:
            click(clicking, lapse=interval)
        time.sleep(lapse)


# 直到匹配模板
def wait_search_template(target: Image.Image, threshold=THR, lapse=0.1):
    while True:
        if search_target(screenshot(), target)[0] > threshold:
            return
        time.sleep(lapse)


# 搜索目标模板存在匹配的最大值
# noinspection PyTypeChecker
def search_target(img: Image.Image, target: Image.Image, mode='cv2') -> float:
    """
    return the maximum of matched
    mode ='cv2'(default) to use open-cv(quick), 'sk' to use skimage package(VERY slow)
    Attention: cv2 use (h,w), but PIL/numpy use (w,h).
    """
    m1: np.ndarray = np.array(img.convert('RGB'))
    m2: np.ndarray = np.array(target.convert('RGB'))
    if mode == 'sk':
        matches: np.ndarray = sk_match_template(m1, m2)
        max_match = np.max(matches)
        pos = np.where(matches == max_match)
        return np.max(matches), (pos[1][0], pos[0][0])
    else:
        cv_img, cv_target = (cv2.cvtColor(m1, cv2.COLOR_RGB2BGR), cv2.cvtColor(m2, cv2.COLOR_RGB2BGR))
        # h, w = cv_target.shape[0:2]
        matches = cv2.matchTemplate(cv_img, cv_target, cv2.TM_CCOEFF_NORMED)
        max_match = np.max(matches)
        pos = np.where(matches == max_match)
        # in PIL system, (x~w,y~h)
        return np.max(matches), (pos[1][0], pos[0][0])


def _test():
    # m1 = screenshot()
    m2 = screenshot()
    t1, t2 = [], []
    reg = (100, 200, 300, 600)
    for i in range(10):
        t0 = time.time()
        wait_which_target(m2, reg)
        t1.append(time.time() - t0)
    print('avg time=%.6f sec' % (np.mean(t1)))
    for i in range(10):
        t0 = time.time()
        wait_which_target(m2, reg)
        t2.append(time.time() - t0)
    print('avg time=%.6f sec' % (np.mean(t2)))

# if __name__ == '__main__':
#     _test()
