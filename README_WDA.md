# WebDriverAgent Installation
iOS version >= 11

Minimum requirements and supported SDKs see:
https://developer.apple.com/support/xcode/

## Homebrew
May need proxy to fetch content.
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

## Xcode
- install Xcode from App Store
  - accept licenses and install components
- `xcode-select --install` to install command-line tools
- `xcode-select --switch /Applications/Xcode.app/Contents/Developer/`
- in Preference/Accounts, add an Apple Developer account, free account is ok.

## Python
Python version >=3.7, only 3.7 and 3.8 are tested.

- `brew install pyenv`
- add following code to the end of `~/.bash_profile`
  ```sh
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"

  if which pyenv > /dev/null;
    then eval "$(pyenv init -)";
  fi
  ```
- `source ~/.bash_profile` or reopen terminal
- `pyenv install 3.8.6`
- `pyenv global 3.8.6`

## Tools
- `brew install carthage` to install dependency manager carthage
- `brew install libimobiledevice --HEAD` for communication with device
- `brew install ideviceinstaller` for installing app
- `gem install xcpretty` only for real device
  - for iOS 10, `cnpm install -g ios-deploy`

## WebDriverAgent
- `git clone https://github.com/appium/WebDriverAgent`
- `cd WebDriverAgent`
- `sh ./Scripts/bootstrap.sh`
- replace string `com.facebook` with a unique identifier like `cc.my_custom` in all project files
    - PyCharm/VS Code is convenient to replace all occurrences in all files
- open `WebDriverAgent.xcodeproj` in Xcode
    - some settings/errors about *_tvOS could be ignored
    - `Signing & Capabilities` of every item in `TARGETS` (WebDriverAgentLib and WebDriverAgentRunner are required)
        - choose `Team`, ensure there is no error.
    - set following iOS deploy target version <= your device iOS version, at least iOS 11.0
        - Project `WebDriverRunner`-`Info`: iOS Deploy Target
        - every item of `TARGETS` - `General`: Deploy Info (iPhone/iPad part)
    - select scheme in menu: Product-Scheme-WebDriverAgentRunner
    - connect iPhone with USB and select device in menu: Product-Destination-YourDevice
    - run Product-Test, then WebDriverAgent should be installed on your device
      - uninstall the old WDA test app if another WDA is used before (mainly causing signature problems)
      - if first run, Xcode will alert "Could not launch WebDriverAgentRunner - Security", 
      trust developer's profile in phone's settings(iPhone-Settings-General-Profiles & Device Management).
      - then run test again, Xcode project should be testing WDA now.
      - **you can also run test in terminal use `xcodebuild`**
      - `xcodebuild -project WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination 'id=<id>' test`
- in Terminal, run `iproxy LOCAL_PORT:DEVICE_PORT`(usually `iproxy 8100 8100`) to map your device's port to localhost
- open any browser, visit `http://localhost:8100/status`, a json response about test and device info will be returned.

## Master-Alterego
Check [README](./README.md) for details.
- edit config file
    - `is_wda`: `True`
    - `wda_url`: `http://localhost:8100` or `null` to use default url
- battle procedure in `battles.py`
    - uncomment and set correct value of `LOC.relocate([x1,y1,x2,y2])` if your device resolution is not 1920*1080

## For Later Running
- connect iPhone to macOS with USB
- run Xcode Test through Xcode.app or xcodebuild command
- proxy device port to localhost, run `iproxy 8100 8100`
- finally run python scripts