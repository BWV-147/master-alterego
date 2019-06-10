import numpy as np
from PIL import ImageGrab
import cv2
from skimage.measure import compare_ssim
from base import *


# image processing
def screenshot(region=(0, 0, 1920, 1080), filepath: str = None):
    # noinspection PyBroadException
    try:
        _image = ImageGrab.grab(region)
    except Exception as e:
        logger.error('grab screenshot failed, return default loading image.\n%s' % e)
        _image = Image.open('./img/loading.png')
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
    if method == 'ssim':
        # noinspection PyTypeChecker
        sim = compare_ssim(np.array(img1), np.array(img2), multichannel=True)
    elif method == 'hist':
        size = tuple(np.min((img1.size, img2.size), 0))
        if size != img1.size:
            img1 = img1.resize(size)
            img2 = img2.resize(size)
        lh = img1.convert('RGB').histogram()
        rh = img2.convert('RGB').histogram()

        sim = sum(1 - (0 if _l == _r else float(abs(_l - _r)) / max(_l, _r)) for _l, _r in zip(lh, rh)) / len(lh)
    else:
        raise ValueError(f'invalid method "{method}", only ssim and hist supported')
    return sim


def match_target(img: Image.Image, target: Image.Image, threshold=THR):
    """
    match locations where similarity >= threshold.
    :return: list of locations (left,top)=(x, y).
    Attention: cv2 use (h,w), but PIL/numpy use (w,h).
    """
    # noinspection PyTypeChecker
    cv_img, cv_target = (cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR),
                         cv2.cvtColor(np.array(target), cv2.COLOR_RGB2BGR))
    h, w = cv_target.shape[0:2]
    matches = cv2.matchTemplate(cv_img, cv_target, cv2.TM_CCOEFF_NORMED)
    loc_all = np.where(matches >= threshold)
    locs = []
    for y, x in zip(*loc_all):
        locs.append((x, y))
        cv2.rectangle(cv_img, (x, y), (x + w, y + h), (0, 0, 250), 2)
        Image.fromarray(cv_img).show()
    return locs


def _wait_region(target, region, threshold=THR, lapse=0.1, at=None, clicking=None):
    # type:(Image.Image,tuple,float,float,Union[bool,tuple],tuple)->None
    """
    .. deprecated::0.0
    Use :func:`wait_regions` instead.
    """
    sim = cal_sim(screenshot(), target, region)
    while sim < threshold:
        if clicking is not None:
            time.sleep(0.5)
            click(clicking)
        sim = cal_sim(screenshot(), target, region)
    if at is True:
        click(region)
    elif isinstance(at, (tuple, list)):
        click(at)
    time.sleep(lapse)

    pass


def wait_regions(targets, regions, threshold=THR, lapse=0.1, at=None, clicking=None):
    # type:(Union[Image.Image,tuple,list],Union[list,tuple],float,float,Union[bool,tuple,list],Union[list,tuple])->int
    """
    Waiting for screenshot matching the region of some target.
    :param targets: an Image or list of Image.
    :param regions: corresponding region to target.
    :param threshold:
    :param lapse:
    :param at:  if True, click the region which screenshot matches,
                if a region, click the region `at`.
    :param clicking: a region to click at until screenshot matches some target
    :return: the index which target matches.
    """
    if isinstance(targets, Image.Image):
        targets = [targets]
        regions = [regions]
    num = len(targets)
    assert len(regions) == num, (targets, regions)
    res = None
    while True:
        shot = screenshot()
        for i in range(num):
            sim = cal_sim(shot, targets[i], regions[i])
            if sim > threshold:
                res = i
                break
            elif clicking is not None:
                time.sleep(0.5)
                click(clicking)
        if res is not None:
            if at is True:
                click(regions[res])
            elif isinstance(at, (tuple, list)):
                click(at)
            time.sleep(lapse)
            break
    return res


def wait_match(target: Image.Image, threshold=THR, lapse=0.1):
    while True:
        locs = match_target(screenshot(), target, threshold)
        # logger.debug('locs= ', locs)
        if locs:
            return locs
        time.sleep(lapse)


def compare_region(img, target, region=None, threshold=THR, at=None):
    # type:(Image.Image,Image.Image,Union[tuple,list],float,Union[bool,tuple,list])->bool
    """
    compare two image at `region`, click `at` if matches. use `screenshot()` as img if img is None
    :return: bool: match or not
    """
    if img is None:
        img = screenshot()
    sim = cal_sim(target.crop(region), img.crop(region))
    if sim > threshold:
        if at is True:
            click(region)
        elif isinstance(at, (tuple, list)):
            click(at)
        return True
    return False


def _test():
    # m1 = screenshot()
    m2 = screenshot()
    t1, t2 = [], []
    reg = (100, 200, 300, 600)
    for i in range(10):
        t0 = time.time()
        _wait_region(m2, reg)
        t1.append(time.time() - t0)
    print('avg time=%.6f sec' % (np.mean(t1)))
    for i in range(10):
        t0 = time.time()
        _wait_region(m2, reg)
        t2.append(time.time() - t0)
    print('avg time=%.6f sec' % (np.mean(t2)))


if __name__ == '__main__':
    _test()
