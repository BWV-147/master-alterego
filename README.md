# Master Alterego

**ぐだ子の分身、クラスはオルターエゴでち。**

**An assist agent to help master play FGO based on image analysis.**

## Requirements
- Python: 3.7
    - as `goto-statement` not adapt Python 3.8 or higher,
    remove all occurrences of these 3 statements if you want to run in 3.8 or higher
    ```
  @with_goto
  goto xxx
  label xxx
  ```
- OS:
    - Windows + Android or iOS emulator
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
- clone this repository and activate virtual environment, e.g. `venv`, `conda`. Use `pip` to install require libraries.
    ```Shell
    pip install -r requirements.txt
    ```

- `python main.py --gen-config` to generate default config file.
- edit config file, default config file will be saved at `data/config.json` once run. See Configuration part for details.
- capture desired template screenshots of running app to `img/` folder. Frequently used templates are listed in `template.py`.
- `python main.py` to start battles. Append `-h` for arguments help.

## WebDriverAgent
For WDA+iOS users, you need an Apple developer account to deploy WDA to your device. See [README_WDA](./README_WDA.md) or following links for details.
 - [appium/WebDriverAgent](https://github.com/appium/WebDriverAgent)
 - [python-wda](https://github.com/openatx/facebook-wda)
 - some blogs, appium test kit is not required:
    - https://www.jianshu.com/p/8be4718ee179
    - https://testerhome.com/topics/8375
    - https://blog.csdn.net/bibi1003/article/details/87182731

# Troubleshooting
**Permission problems**
- Windows: run script as admin, since most emulators run as admin. A program run without admin permission could not take interaction(like click) with those run as admin.
- macOS+emulator: grant `Screen Recording` and `Accessibility` permissions for program who start python script(PyCharm/Terminal...)

**WDA Orientation**
- try set screenshotOrientation to portrait or landscapeLeft/Right...


## TODO
- change config file on served webpage
- kizuna->clicking->rewards, kizuna page should be optional, and add rewards-init page
- add param to check master cloth at team page
- play card check: no floating if checked
- move supervisor from main thread to child thread
- save more than one battle in config.battles{battle_name:battle}, then specific battle_name
- capture android emulator's screenshot directly rather take windows' screen.
