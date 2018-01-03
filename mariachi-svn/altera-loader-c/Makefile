CC=gcc
CFLAGS=-lftd2xx
# -Wl,-rpath /usr/local/lib

APP = alterald

all: $(APP)

$(APP): $(APP).c	
	$(CC) -o $(APP) $(CFLAGS) $(APP).c

clean:
	rm -f *.o ; rm $(APP)
