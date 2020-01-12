<h1 align="center">
  <img src="https://github.com/Dreamacro/clash/raw/master/docs/logo.png" alt="Clash" width="200">
  <br>auto-clash-update<br>
</h1>

<h4 align="center">Automatically update your clash profiles</h4>
<p align="center">
   <a href="https://www.codacy.com/manual/carottX/auto-clash-update?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=carottX/auto-clash-update&amp;utm_campaign=Badge_Grade">
      <img src="https://api.codacy.com/project/badge/Grade/61688f05731b4356a44ded084b1485d6">
   </a>
 </p>

## config.json Usage

clash_config_path: Where your actual clash config is

config: Profiles' details

custom_header: Header for requesting profile files

auto_save: Whether auto write config to file each time you modify

## Usage
 ```sh
git clone git@github.com:carottX/auto-clash-update.git
cp config.json.example config.json
chmod +x getyaml.py
./getyaml.py
 ``` 
## Thanks

[Dreamacro-clash](https://github.com/Dreamacro/clash)
