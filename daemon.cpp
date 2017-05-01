#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <unistd.h>
#include <cstdio>

int main(){
	char str[132072];
	char filename[] = "/etc/mycron.cfg";
	std::ifstream inp(filename, std::ifstream::in);
	inp.getline(str, 132071);
	long long n = strtoll(str, NULL, 10);
	inp.getline(str, 132071);
	inp.close();
	//fprintf(stderr, "%lld %s\n", n, str);
	//system(str);
	while (true){
		sleep(60*n);
		system(str);
	}
	return 0;
}
