#pragma once
#include "wsqueue.h"
#include <stddef.h>
#define container_of(ptr, type, member) (type*)((char*)(ptr) - offsetof(type, member))

struct Task {
	void (*f)(void *); 
	void* arg; 
	pthread_cond_t cond;
	pthread_mutex_t mutex;
	struct list_node node;
	volatile int done;
	size_t child_num;
	struct Task** child;
};

struct ThreadPool {
	struct wsqueue tasks;
	pthread_t* threads;
	size_t thread_number;
};

void thpool_init(struct ThreadPool* pool, size_t threads_nm); 
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task); 
void thpool_finit(struct ThreadPool* pool);

void task_init(struct Task* task, void (*f) (void*), void* arg);
void task_finit(struct Task* task);
