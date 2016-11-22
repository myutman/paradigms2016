#include "thread_pool.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <assert.h>

size_t rec_limit;
pthread_mutex_t rand_mutex;

int random(){
	pthread_mutex_lock(&rand_mutex);
	int ans = rand();
	pthread_mutex_unlock(&rand_mutex);
	return ans;
}

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
	struct Arg* tmp = (struct Arg*) arg;
	int* array = tmp->array;
	size_t n = tmp->n;
	size_t dep = tmp->dep;
	//fprintf(stderr, "%d %d\n", (int)dep, (int)n);
	struct Task* task = &tmp->task;

	if (dep == rec_limit){
		//fprintf(stderr, "inq\n");
		qsort(array, n, sizeof(int), intcmp);
		//fprintf(stderr, "outq\n");
		return;
	}
	if (n <= 1) return;
	int x = array[random() % n];
	//int x = array[n / 2];
	int *l = array;
	int *r = array + n - 1;
	while (l < r){
		while (*l < x && l < r) l++;
		while (*r >= x && r > l) r--;
		if (l < r) swap(l, r);
	}

	struct Arg* arg1 = malloc(sizeof(struct Arg));
	struct Arg* arg2 = malloc(sizeof(struct Arg));

	arg1->array = array;
	arg1->n = l - array;
	arg1->dep = dep + 1;
	task_init(&arg1->task, f, arg1);

	arg2->array = l;
	arg2->n = n - (l - array);
	arg2->dep = dep + 1;
	task_init(&arg2->task, f, arg2);

	task->child = malloc(2 * sizeof(struct Task*));
	task->child[0] = &arg1->task;
	task->child[1] = &arg2->task;
	task->child_num	= 2;

	thpool_submit(&tpool, &arg1->task);
	thpool_submit(&tpool, &arg2->task);

	//fprintf(stderr, "%d %d back\n", (int)dep, (int)n);
}

int main(int argc, char* argv[]) {
	pthread_mutex_init(&rand_mutex, NULL);
	double t = clock();
	srand(42);
	size_t threads_nm, n;
	if (argc < 4){
        threads_nm = 1;
        n = 10;
        rec_limit = 4;
	}
    else {
        threads_nm = atoi(argv[1]);
        n = atoi(argv[2]);
        rec_limit = atoi(argv[3]);
	}
	int* array = malloc(n * sizeof(int));
	//fprintf(stderr, "%d\n", (int)(n * sizeof(int)));
	for (size_t i = 0; i < n; i++){
		array[i] = random();
		//fprintf(stderr, "%d\n", array[i]);
	}
	struct Arg* arg = malloc(sizeof(struct Arg));
	arg->array = array;
	arg->n = n;
	arg->dep = 0;
	task_init(&arg->task, f, arg);
	//tpool = malloc(sizeof(struct ThreadPool));
	thpool_init(&tpool, threads_nm);
	thpool_submit(&tpool, &arg->task);
	start_wait(&arg->task);

	//fprintf(stderr, "hello\n");

	thpool_finit(&tpool);
	int sorted = 1;
	for (size_t i = 1; i < n; i++){
		if (array[i] < array[i - 1]) sorted = 0;
	}
	free(array);
	pthread_mutex_destroy(&rand_mutex);
	if (sorted) fprintf(stderr, "sorted\n");
	else fprintf(stderr, "not sorted:(\n");
	fprintf(stderr, "%.6lf\n", (clock() - t) / CLOCKS_PER_SEC);
	return 0;
}
