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

	struct Task* task = (struct Task*) arg;
	int* array = *((int**)((char*)arg + sizeof(struct Task)));
	size_t n = *((size_t*)((char*)arg + sizeof(struct Task) + sizeof(int*)));
	size_t dep = *((size_t*)((char*)arg + sizeof(struct Task) + sizeof(int*) + sizeof(size_t)));

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

	void* arg1 = malloc(sizeof(struct Task) + sizeof(int*) + sizeof(size_t) + sizeof(size_t));
	task_init(arg1, f, arg1);
	*((int**)((char*)arg1 + sizeof(struct Task))) = array;
	*((size_t*)((char*)arg1 + sizeof(struct Task) + sizeof(int*))) = l - array;
	*((size_t*)((char*)arg1 + sizeof(struct Task) + sizeof(int*) + sizeof(size_t))) = dep + 1;

    void* arg2 = malloc(sizeof(struct Task) + sizeof(int*) + sizeof(size_t) + sizeof(size_t));
	task_init(arg2, f, arg2);
	*((int**)((char*)arg2 + sizeof(struct Task))) = l;
	*((size_t*)((char*)arg2 + sizeof(struct Task) + sizeof(int*))) = n - (l - array);
	*((size_t*)((char*)arg2 + sizeof(struct Task) + sizeof(int*) + sizeof(size_t))) = dep + 1;

	task->child = malloc(2 * sizeof(struct Task*));
	task->child[0] = (struct Task*) arg1;
	task->child[1] = (struct Task*) arg2;
	task->child_num	= 2;

	thpool_submit(&tpool, (struct Task*) arg1);
	thpool_submit(&tpool, (struct Task*) arg2);

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
	void* arg = malloc(sizeof(struct Task) + sizeof(int*) + sizeof(size_t) + sizeof(size_t));
	task_init(arg, f, (struct Task*) arg);
	*((int**)((char*)arg + sizeof(struct Task))) = array;
	*((size_t*)((char*)arg + sizeof(struct Task) + sizeof(int*))) = n;
	*((size_t*)((char*)arg + sizeof(struct Task) + sizeof(int*) + sizeof(size_t))) = 0;
	//tpool = malloc(sizeof(struct ThreadPool));
	thpool_init(&tpool, threads_nm);
	thpool_submit(&tpool, (struct Task*) arg);
	start_wait((struct Task*) arg);

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
