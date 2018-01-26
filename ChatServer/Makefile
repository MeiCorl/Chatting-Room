CC = g++
CFLAGS = -g
  
all: clean Room.o utils.o ChatServer.o ChatServer  
  
Room.o: Room.h  
	${CC} ${CFLAGS} -c Room.cpp  

utils.o: utils.h
	${CC} ${CFLAGS} -c utils.cpp 

ChatServer.o: Room.h  
	${CC} ${CFLAGS} -c ChatServer.cpp  
  
ChatServer: Room.o ChatServer.o  
	${CC} ${CFLAGS} Room.o ChatServer.o utils.o -l event -l json -o ChatServer  
clean:  
	rm -rf *.o  
	rm -rf ChatServer 