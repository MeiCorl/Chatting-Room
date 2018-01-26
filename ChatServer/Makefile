CC = g++
CFLAGS = -g
  
all: clean Room.o DBHelper.o ChatServer.o ChatServer  
  
Room.o: Room.h  
	${CC} ${CFLAGS} -c Room.cpp  

DBHelper.o: DBHelper.h
	${CC} ${CFLAGS} -c DBHelper.cpp 

ChatServer.o: Room.h  
	${CC} ${CFLAGS} -c ChatServer.cpp  
  
ChatServer: Room.o ChatServer.o  
	${CC} ${CFLAGS} Room.o ChatServer.o DBHelper.o -l event -l json -l mysqlcppconn -o ChatServer  
clean:  
	rm -rf *.o  
	rm -rf ChatServer 