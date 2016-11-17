CC      ?= gcc
CFLAGS  ?= -Wall -Wextra -Werror -std=c99 -g
LDFLAGS ?= -lpthread

all: msgqueue

msgqueue: pqsort.o thread_pool.o linkedlist.o queue.o squeue.o wsqueue.o
	$(CC) pqsort.o thread_pool.o linkedlist.o queue.o squeue.o wsqueue.o \
		$(LDFLAGS) -o pqsort

pqsort.o: pqsort.c
	$(CC) -c pqsort.c $(CFLAGS) -o pqsort.o

thread_pool.o: thread_pool.c
	$(CC) -c thread_pool.c $(CFLAGS) -o thread_pool.o

linkedlist.o: linkedlist.c
	$(CC) -c linkedlist.c $(CFLAGS) -o linkedlist.o

queue.o: queue.c
	$(CC) -c queue.c $(CFLAGS) -o queue.o

squeue.o: squeue.c
	$(CC) -c squeue.c $(CFLAGS) -o squeue.o

wsqueue.o: wsqueue.c
	$(CC) -c wsqueue.c $(CFLAGS) -o wsqueue.o

clean:
	rm *.o pqsort

.PHONY: clean
