

all:
	python ./src/main.py $(arg)

prepdll:./src/main.c
	gcc ./src/main.c -shared -o mouse_click.dll  -luser32

run:c_code
	./a.exe

c_code:./src/main.c
	gcc ./src/main.c -o a.exe -luser32