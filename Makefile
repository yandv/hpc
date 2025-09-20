CC = gcc
CFLAGS = -Wall -O2
OMPFLAGS = -fopenmp
BINDIR = out
SRCDIR = src

all: 
	mkdir -p $(BINDIR)
	$(MAKE) sort_parallel
	$(MAKE) sort
	$(MAKE) generate
	$(MAKE) check

sort_parallel: $(SRCDIR)/sort_parallel.c
	$(CC) $(CFLAGS) $(OMPFLAGS) -o $(BINDIR)/sort_parallel.exe $(SRCDIR)/sort_parallel.c

sort: $(SRCDIR)/sort.c
	$(CC) $(CFLAGS) -o $(BINDIR)/sort.exe $(SRCDIR)/sort.c

generate: $(SRCDIR)/generate.c
	$(CC) $(CFLAGS) -o $(BINDIR)/generate.exe $(SRCDIR)/generate.c

check: $(SRCDIR)/check_sort.c
	$(CC) $(CFLAGS) -o $(BINDIR)/check_sort.exe $(SRCDIR)/check_sort.c

clean:
	rm -f $(BINDIR)/*.exe

.PHONY: all clean
