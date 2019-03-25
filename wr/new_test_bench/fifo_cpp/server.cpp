/*
     add_server.c: A server to add numbers received in message.

 */

#define SERVER_FIFO "/tmp/addition_fifo_server"
#define MAX_NUMBERS 500

#include "handy.h"

int main(int argc, char **argv)
{
	int fd, fd_client, bytes_read, i;
	char buf[4096];
	char *return_fifo;
	char *numbers[MAX_NUMBERS];

	if ((mkfifo(SERVER_FIFO, 0664) == -1) && (errno != EEXIST)) {
		perror("mkfifo");
		exit(1);
	}
	if ((fd = open(SERVER_FIFO, O_RDONLY)) == -1) perror("open");

	while (1) {
		// get a message
		memset(buf, '\0', sizeof(buf));
		if ((bytes_read = read(fd, buf, sizeof(buf))) == -1)
			perror("read");
		if (bytes_read == 0) continue;

		if (bytes_read > 0) {
			if (close(fd_client) == -1) perror("close");
			cout_time_nano();
			return 0;
		}
	}
}