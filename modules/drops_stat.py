import re

from util.autogui import *


# O=(233,187,409,379)
# dx=206
# dy=213
# w=176
# h=192
class DropsStat:
    def __init__(self):
        self.images: Dict[str, Image.Image] = {}
        self.LOC = Regions()
        # self.LOC.relocate()
        self.item_templates: Dict[str, Image.Image] = {}
        self.stat_results: Dict[str, int] = {}
        self._no, self._num = 0, len(self.images)
        pass

    def load_item_template(self, directory: str, *item_locs):
        """
        :param directory:
        :param item_locs: [item_name, img_fn, row, column]
        :return:
        """
        for filename in os.listdir(directory):
            matched = re.findall(r'rewards-(.*?)-([\d\-]+).png', filename)
            if matched:
                self.images[filename] = Image.open(os.path.join(directory, filename))
        for item_name, img_fn, row, column in item_locs:
            assert img_fn in self.images and 0 <= row <= 2 and 0 <= column <= 6
            self.item_templates[item_name] = self.images[img_fn].crop(self.LOC.rewards_items[row][column])

    def calc(self):
        self.stat_results.clear()

        from concurrent.futures import ThreadPoolExecutor
        executor = ThreadPoolExecutor(max_workers=20)
        for _ in executor.map(self._cal_one, list(self.images.keys())):
            # print(res)
            pass
        print(f'All {self._num} finished.')
        self.print_results()

    def _cal_one(self, fn):
        img = self.images[fn]
        for i in range(3):
            for j in range(7):
                if i == j == 0:
                    continue
                outer = img.crop(self.LOC.rewards_items_outer[i][j])
                match_res = []
                for item_name, tmpl in self.item_templates.items():
                    match_res.append([item_name, search_target(outer, tmpl)[0]])
                match_res.sort(key=lambda o: o[1], reverse=True)
                match_item, match_prob = match_res[0]
                if match_res[0][1] > 0.95:
                    self.stat_results[match_item] = self.stat_results.get(match_item, 0) + 1
        self._no += 1
        print(f'\rprogress {self._no}/{self._num} ...\r', end='')

    def print_results(self):
        print(f'===== Results =====')
        print(f'image num: {self._num}')
        print(f'items num: {self.stat_results}')


# %%
if __name__ == '__main__':
    stat = DropsStat()
    # rewards-Bone-0316-1818.png: bone-0-1,gold-0-5,red-0-6,
    # rewards-Bone-0316-1941.png: blue-0-4,fire4-0-5,fire5-1,3
    fns = ['rewards-Bone-0316-1818.png', 'rewards-Bone-0316-1941.png']
    stat.load_item_template('img/_drops', ['凶骨', fns[0], 0, 1], ['剑秘', fns[0], 0, 5], ['剑魔', fns[0], 0, 6],
                            ['剑辉', fns[1], 0, 4], ['火四', fns[1], 0, 5], ['火五', fns[1], 1, 3])
    stat.calc()
