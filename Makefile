

all:
	python ./src/main.py $(arg)

run:c_code
	./a.exe

c_code:./src/main.c
	gcc ./src/main.c -o a.exe -luser32