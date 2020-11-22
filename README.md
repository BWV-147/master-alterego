# Master Alterego

**ぐだ子の分身、クラスはオルターエゴでち。**

**An assist agent to help master play FGO based on image analysis.**

## Support Platforms
- Python: 3.7 (higher versions are not tested)
- OS:
    - Windows + Android or iOS emulator
        - keep running at foreground, usually fullscreen
    - macOS + Android emulator (not tested)
    - macOS + iOS real device
        - Xcode developer account
        - use WebDriverAgent to communicate with iOS device

## Directory Structure:
- `data/`: config files and other resources like sound file.
- `img/`: all template images.
    - `img/_drops/`: saved screenshots of reward pages.
    - `img/share/{device}`: shared image templates for reuse.
    - `img/battles/{battle_name}`: templates for specific free battle.
- `logs/`: app/server logs.
- `modules/` and `util/`
- `www/`: server root
- `battles.py`: edit your battle procedures here.
- `main.py`: main entrance.
- `template.py`: used template screenshots are listed.


## Usage
First clone this repository and activate virtual environment, e.g. `venv`, `conda`. Use `pip` to install require libraries.
```Shell
pip install -r requirements.txt
```

Edit config file, default config file will be saved at `data/config.json` once run. See Configuration part for details.

Capture desired template screenshots of running app to `img/` folder. Frequently used templates are listed in `template.py`.

Start script `python main.py`. Append `-h` for arguments help.

## WebDriverAgent
For WDA+iOS users, you need an Apple developer account to deploy WDA to your device. See following links for details.
 - [appium/WebDriverAgent](https://github.com/appium/WebDriverAgent)
 - [python-wda](https://github.com/openatx/facebook-wda)
 - some blogs, appium test kit is not required:
    - https://www.jianshu.com/p/8be4718ee179
    - https://testerhome.com/topics/8375
    - https://blog.csdn.net/bibi1003/article/details/87182731

## TODO
- change config file on served webpage
- kizuna->clicking->rewards, kizuna page should be optional, and add rewards-init page
- add param to check master cloth at team page
- play card check: no floating if checked
- move supervisor from main thread to child thread
