## This is the c program for transmitting files through websocket

### Compile
`make`

### Usage

`server.c` is the receiver. Start it first, like `./server output.txt 17777`

`client.c` is the sender. Use it after `server.c` has started, like `./client input.txt 127.0.0.1 17777`

Then `input.txt` will be sent to `127.0.0.1:17777` as `output.txt`.

### Advanced

#### FEATURE-1 
Break after 1 file is received.

#### FEATURE-2
Measure time spent

