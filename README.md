# Master Alterego

**ぐだ子の分身、クラスはオルターエゴでち。**

**An assist agent to help master play FGO based on image analysis.**

## Requirements
- Python: 3.7
    - since `goto-statement` not adapted for Python 3.8 or higher, `@with_goto`, `goto`and `label` take no effect.
- OS:
    - **IMPORTANT**: full screen display won't be adapted, valid render region must be **16:9**
    - Windows + Android/iOS emulator
        - keep running at foreground, usually fullscreen
    - macOS + Android emulator (not tested)
    - macOS + iOS real device
        - Apple developer account
        - use WebDriverAgent to communicate with iOS device

## File Structure:
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
- clone this repository and activate virtual environment, e.g. `venv`, `conda`. Use `pip` to install required libraries.
    ```Shell
    pip install -r requirements.txt
    ```

- `python main.py --gen-config` to generate default config file at `data/config.json`.
- edit config file. See Configuration part for details.
- capture desired template screenshots of running app to `img/` folder. Frequently used templates are listed in `template.py`.
- `python main.py` to start battles. Append `-h` for arguments help.

## WebDriverAgent
For WDA+iOS users, you need an Apple developer account to deploy WDA to your device. See [README_WDA](./README_WDA.md) or following links for details.
 - [appium/WebDriverAgent](https://github.com/appium/WebDriverAgent)
 - [python-wda](https://github.com/openatx/facebook-wda)
 - some blogs, appium test kit is not required:
    - https://github.com/appium/appium-xcuitest-driver/blob/master/docs/real-device-config.md
    - https://www.jianshu.com/p/8be4718ee179
    - https://testerhome.com/topics/8375
    - https://blog.csdn.net/bibi1003/article/details/87182731

# Troubleshooting
**Permission problems**
- Windows: run script as admin, since most emulators run as admin. A program run without admin permission could not take interaction(like click) with those run as admin.
- macOS+emulator: grant `Screen Recording` and `Accessibility` permissions for program who start python script(PyCharm/Terminal...)

**WDA Orientation**
- try set screenshotOrientation to portrait or landscapeLeft/Right...

**Xcode certification**
- test failed because of security: trust profile in Settings-General-Profiles (network connection needed)
- signing certificate will be expired in 6 days for free developer account,
 restart Xcode and signing again to refresh
- access security of keychains for new generated certificate

## TODO
- kizuna->clicking->rewards, kizuna page should be optional, and add rewards-init page
- add param to check master cloth at team page
- play card check: no floating if checked
- capture android emulator's screenshot directly rather take windows' screen.
