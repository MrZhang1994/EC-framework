/*
     add_client.c: Client program to take user input comprising
		   of numbers, send request message to add_server
		   and receive server's response

 */

#include "handy.h"

#define SERVER_FIFO "/tmp/addition_fifo_server"

char my_fifo_name[128];
char buf1[512], buf2[1024];

int main(int argc, char **argv)
{
	int fd, fd_server, bytes_read;

	// make client fifo
	sprintf(my_fifo_name, "/tmp/add_client_fifo%ld", (long)getpid());

	if (mkfifo(my_fifo_name, 0664) == -1) perror("mkfifo");

	int it = 0;
	int a = 0;
	for (it = 0; it < 1000; it++) {
		a = a + 1;
	}

	while (1) {
		// get user input

		strcpy(buf2, "123");

		// send message to server

		// unsigned long time_in_micros = GetTimeStamp();
		// printf("%ld", time_in_micros);

		cout_time_nano();

		if ((fd_server = open(SERVER_FIFO, O_WRONLY)) == -1) {
			perror("open: server fifo");
			break;
		}

		if (write(fd_server, buf2, strlen(buf2)) != strlen(buf2)) {
			perror("write");
			break;
		}

		if (close(fd_server) == -1) {
			perror("close");
			break;
		}

		break;
	}
}