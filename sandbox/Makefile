all:
	rm -f *.o
	rm -f safeexec
	rm -f os-detect

	gcc -c safe.c -Wall -ansi -pedantic
	gcc -o os-detect os-detect.c -Wall -ansi -pedantic
	gcc -c safeexec.c `./os-detect` -Wall -ansi -pedantic
	gcc -o safeexec safeexec.o safe.o -Wall -ansi -pedantic

	sudo chown root:root safeexec
	sudo chmod u+s safeexec
