"""Image processing and computation"""
import numpy as np
from PIL import ImageGrab
import cv2
from skimage.measure import compare_ssim as sk_compare_ssim
from skimage.feature import match_template as sk_match_template
from dataset import *


def screenshot(region=None, filepath: str = None):
    # noinspection PyBroadException
    try:
        _image = ImageGrab.grab(region)
    except Exception as e:
        logger.error('grab screenshot failed, return default single color image.\n%s' % e)
        _image = Image.new('RGB', (1920, 1080), (0, 255, 255))
        # _image = Image.open('./img/loading.png')
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


def match_target(img: Image.Image, target: Image.Image, mode='sk2'):
    """
    return the maximum of matched
    Attention: cv2 use (h,w), but PIL/numpy use (w,h).
    """
    if mode == 'sk':
        # noinspection PyTypeChecker
        matches: np.ndarray = sk_match_template(np.array(img.convert('RGB')), np.array(target.convert('RGB')))
        return np.max(matches)

    else:
        # noinspection PyTypeChecker
        cv_img, cv_target = (cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2BGR),
                             cv2.cvtColor(np.array(target.convert('RGB')), cv2.COLOR_RGB2BGR))
        # h, w = cv_target.shape[0:2]
        matches = cv2.matchTemplate(cv_img, cv_target, cv2.TM_CCOEFF_NORMED)
        return np.max(matches)


def compare_one_region(img, target, region=None, threshold=THR, at=None):
    # type:(Image.Image,Image.Image,Union[tuple,list],float,Union[bool,tuple,list])->bool
    """
    compare two image at `region`, click `at` if matches. use `screenshot()` as img if img is None
    :return: bool: match or not
    """
    sim = cal_sim(target.crop(region), img.crop(region))
    if sim > threshold:
        if at is True:
            click(region)
        elif isinstance(at, (tuple, list)):
            click(at)
        return True
    return False


def compare_regions(img, targets, regions, threshold=THR, at=None):
    # type:(Image.Image,Union[Image.Image,tuple,list],Union[list,tuple],float,Union[bool,tuple,list])->int
    """
    compare which `target` matches `img` at `region`, click `at` if matches.
    :return: matched index, -1 if not matched.
    """
    if isinstance(targets, Image.Image):
        targets = [targets]
        regions = [regions]
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

    while True:
        shot = screenshot()
        res = compare_regions(shot, targets, regions, threshold, at)
        if res >= 0:
            return res
        if clicking is not None:
            click(clicking, lapse=0.5)
        time.sleep(lapse)


def wait_match(target: Image.Image, threshold=THR, lapse=0.1):
    while True:
        if match_target(screenshot(), target) > threshold:
            return
        time.sleep(lapse)


def _test():
    # m1 = screenshot()
    m2 = screenshot()
    t1, t2 = [], []
    reg = (100, 200, 300, 600)
    for i in range(10):
        t0 = time.time()
        wait_regions(m2, reg)
        t1.append(time.time() - t0)
    print('avg time=%.6f sec' % (np.mean(t1)))
    for i in range(10):
        t0 = time.time()
        wait_regions(m2, reg)
        t2.append(time.time() - t0)
    print('avg time=%.6f sec' % (np.mean(t2)))

# if __name__ == '__main__':
#     _test()
