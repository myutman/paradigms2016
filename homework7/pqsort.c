#include "thread_pool.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <assert.h>

size_t rec_limit;

int intcmp(const void* a, const void* b){
	return (*((int*)a) - *((int*)b));
}

void swap(int* a, int *b){
	int t = *a;
	*a = *b;
	*b = t;
}

struct ThreadPool tpool;

void f (void* arg){

	int* array = *((int**)arg);
	size_t n = *((size_t*)((char*)arg + sizeof(int*)));
	size_t dep = *((size_t*)((char*)arg + sizeof(int*) + sizeof(size_t)));
	//fprintf(stderr, "%d %d\n", (int)dep, (int)n);
	struct Task* task = *((struct Task**)((char*)arg + sizeof(int*) + 2 * sizeof(size_t)));

	free(arg);
	if (dep == rec_limit){
		//fprintf(stderr, "inq\n");
		qsort(array, n, sizeof(int), intcmp);
		//fprintf(stderr, "outq\n");
		return;
	}
	if (n <= 1) return;
	int x = array[rand() % n];
	int *l = array;
	int *r = array + n - 1;
	while (l < r){
		while (*l < x && l < r) l++;
		while (*r > x && r > l) r--;
		if (l < r) swap(l, r);
	}

	struct Task* task1 = malloc(sizeof(struct Task));
	struct Task* task2 = malloc(sizeof(struct Task));

	void* arg1 = malloc(sizeof(int*) + sizeof(size_t) + sizeof(size_t) + sizeof(struct Task*));
	*((int**)arg1) = array;
	*((size_t*)((char*)arg1 + sizeof(int*))) = l - array;
	*((size_t*)((char*)arg1 + sizeof(int*) + sizeof(size_t))) = dep + 1;
	*((struct Task**)((char*)arg1 + sizeof(int*) + 2 * sizeof(size_t))) = task1;

	void* arg2 = malloc(sizeof(int*) + sizeof(size_t) + sizeof(size_t) + sizeof(struct Task*));
	*((int**)arg2) = array;
	*((size_t*)((char*)arg2 + sizeof(int*))) = n - (l - array);
	*((size_t*)((char*)arg2 + sizeof(int*) + sizeof(size_t))) = dep + 1;
	*((struct Task**)((char*)arg2 + sizeof(int*) + 2 * sizeof(size_t))) = task2;

	task_init(task1, f, arg1);
	task_init(task2, f, arg2);

	task->child = malloc(2 * sizeof(struct Task*));
	task->child[0] = task1;
	task->child[1] = task2;
	task->child_num	= 2;

	thpool_submit(&tpool, task1);
	thpool_submit(&tpool, task2);

	//fprintf(stderr, "%d %d back\n", (int)dep, (int)n);
}

int ct = 0;

void start_wait(struct Task* task){
	thpool_wait(task);
	ct++;
	fprintf(stderr, "%d\n", ct);
	for (size_t i = 0; i < task->child_num; i++)
		start_wait(task->child[i]);
	task_finit(task);
	free(task);
}

int main(int argc, char* argv[]) {
	double t = clock();
	//srand(time(NULL));
	size_t threads_nm, n;
	if (argc < 4){
        threads_nm = 4;
        n = 500000;
        rec_limit = 15;
	}
    else {
        threads_nm = atoi(argv[1]);
        n = atoi(argv[2]);
        rec_limit = atoi(argv[3]);
	}
	int* array = malloc(n * sizeof(int));
	//fprintf(stderr, "%d\n", (int)(n * sizeof(int)));
	for (size_t i = 0; i < n; i++){
		array[i] = rand();
		//fprintf(stderr, "%d\n", array[i]);
	}
	struct Task* task = malloc(sizeof(struct Task));
	void* arg = malloc(sizeof(int*) + sizeof(size_t) + sizeof(size_t) + sizeof(struct Task*));
	*((int**)arg) = array;
	*((size_t*)((char*)arg + sizeof(int*))) = n;
	*((size_t*)((char*)arg + sizeof(int*) + sizeof(size_t))) = 0;
	*((struct Task**)((char*)arg + sizeof(int*) + 2 * sizeof(size_t))) = task;
	task_init(task, f, arg);
	//tpool = malloc(sizeof(struct ThreadPool));
	thpool_init(&tpool, threads_nm);
	thpool_submit(&tpool, task);
	start_wait(task);

	fprintf(stderr, "hello\n");

	thpool_finit(&tpool);
	printf("%d\n", (int)n);
	for (size_t i = 0; i < n; i++){
		printf("%d ", array[i]);
	}
	free(array);
	fprintf(stderr, "%.6lf\n", (clock() - t) / CLOCKS_PER_SEC);
	return 0;
}
