#include <errno.h>
#include <error.h>
#include <fcntl.h>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>
#include <chrono>
#include <ctime>
#include <iostream>
#include <ratio>
#include "date.h"

void cout_time_nano()
{
	using namespace std::chrono;
	std::cout << date::format(
	    "%F %T\n", time_point_cast<nanoseconds>(system_clock::now()));
}