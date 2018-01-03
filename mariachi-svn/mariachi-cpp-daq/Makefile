CC=g++
CFLAGS=-lftd2xx

APP = daq.exe

all: $(APP)

$(APP): mdaq.cxx	
	$(CC) -o $(APP) $(CFLAGS) mdaq.cxx

clean:
	rm -f *.o ; rm $(APP)
