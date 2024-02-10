# RushRoyale Bot automations

## 2024-Feb-10:14-02-26 PM STILL UNDERDEVELOPMENT
```diff
- don't use this .
- this is stilll under development
- currently the click event is not being registred to game window
- but mspaint and other application are responding to the event
```



# dependencies

1) Python with `pip`, [`venv` optional]
```console
# [optional]
python -m venv .virtual

#[linux/unix]
source .virtual/bin/activate 
# or #[ps1/windows]
.virtual\Scripts\activate 
```

```console
    python -m pip install -r requ.txt
``` 
2) RushRoyale game [window version](https://rr.my.games/en), [Download Now](https://static.gc.my.games/RushRoyaleLoader.exe);
    no need to resize or anything just sigin into game an run

# How to use

1) Using Makefile
    requires `make` if you want to use make other wise you can run 
    manually 
```console
make
```
2) Manually
```console
    python ./src/main.py 
```