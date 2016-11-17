#include "thread_pool.h"
#include <stdlib.h>
#include <stdio.h>

static volatile int cont = 1;

void *doit(void* data){
	struct ThreadPool* pool = *((struct ThreadPool**)data);
	//int i = *((int *)(data + sizeof(struct ThreadPool*)));
	while (cont || queue_size(&pool->tasks.squeue.queue)){
		struct list_node *node;
		
		pthread_mutex_lock(&pool->tasks.squeue.mutex);
		while (cont && !queue_size(&pool->tasks.squeue.queue))
			pthread_cond_wait(&pool->tasks.cond, &pool->tasks.squeue.mutex);
		pthread_mutex_unlock(&pool->tasks.squeue.mutex);
				
		if (queue_size(&pool->tasks.squeue.queue)){
			node = wsqueue_pop(&pool->tasks);			
			struct Task* task = container_of(node, struct Task, node);		
			task->f(task->arg);
			task->done = 1;
			pthread_mutex_lock(&task->mutex);		
			pthread_cond_signal(&task->cond);
			pthread_mutex_unlock(&task->mutex);
		}
	}
	return NULL;
}

void thpool_init(struct ThreadPool* pool, size_t threads_nm){
	wsqueue_init(&pool->tasks);
	pool->thread_number = threads_nm;
	pool->threads = malloc(sizeof(pthread_t) * threads_nm);
	for (size_t i = 0; i < threads_nm; i++){
		//void* arg = malloc(sizeof(struct ThreadPool*) + sizeof(int));
		//*arg = pool;
		//*(arg + sizeof(struct ThreadPool*)) = &i;
		pthread_create(pool->threads + i, NULL, doit, &pool);
		//free(arg);
	}
}

void thpool_submit(struct ThreadPool* pool, struct Task* task){
	pthread_mutex_lock(&task->mutex);
	wsqueue_push(&pool->tasks, &task->node);
	wsqueue_notify(&pool->tasks);
	pthread_mutex_unlock(&task->mutex);
}

void thpool_wait(struct Task* task){
	fprintf(stderr, "hello\n");	
	pthread_mutex_lock(&task->mutex);
	fprintf(stderr, "hello1\n");
	while (!task->done){
		fprintf(stderr, "hello1\n");
		pthread_cond_wait(&task->cond, &task->mutex);
	}
	pthread_mutex_unlock(&task->mutex);	
}

void thpool_finit(struct ThreadPool* pool){
	size_t threads_nm = pool->thread_number;
	cont = 0;	
	wsqueue_notify_all(&pool->tasks);
	for (size_t i = 0; i < threads_nm; i++)
		pthread_join(pool->threads[i], NULL);
	wsqueue_finit(&pool->tasks);
	free(pool->threads);
}

void task_init(struct Task* task, void (*f) (void*), void* arg){
	task->f = f;
	task->arg = arg;
	task->done = 0;
	pthread_cond_init(&task->cond, NULL);
	pthread_mutex_init(&task->mutex, NULL);
	task->child_num = 0;
	task->child = NULL;
	task->node.next = task->node.prev = NULL;
}

void task_finit(struct Task* task){
	pthread_cond_destroy(&task->cond);
	pthread_mutex_destroy(&task->mutex);
	if (task->child_num)
		free(task->child);
}
