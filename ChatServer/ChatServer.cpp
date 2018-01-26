#include "Room.h"
#include "utils.h"
#include <iostream>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include <json/json.h>
#include <event2/event_struct.h>
#include <event2/event.h>
#include <event2/util.h>

#include <vector>
        
const int SERVER_PORT = 1234;
const int roomNumber = 6;
vector<Room*> roomList;
map<int, int> client_room_map;    //   key: client_fd,   value: room_id     表示在线用户和其所在房间id的映射， -1表示在大厅
event_base *evbase;
Utils* util;

void setnonblock(int sock)
{
	int opts;
	opts = fcntl(sock, F_GETFL);
	if (opts < 0)
	{
		perror("fcntl(sock,GETFL)");
		exit(-1);
	}
	opts = opts | O_NONBLOCK;
	if (fcntl(sock, F_SETFL, opts) < 0)
	{
		perror("fcntl(sock,SETFL,opts)");
		exit(-1);
	}
}

void onRead(int fd, short ev, void *arg)
{
	char buf[512];
	int len=read(fd,buf,512);
	if (len <= 0) {  
        cout << "client closed" << endl;  
        // 连接结束(=0)或连接错误(<0)，将事件删除并释放内存空间
        client_room_map.erase(fd);
        util->deleteOnlineUser(fd);
     //   shutdown(fd,SHUT_WR);
        close(fd);  
    //  struct event *pEvRead = (struct event*)arg; 
    //  event_del(pEvRead);  
    //  delete pEvRead;  
    //  event_free((struct event*)arg);
        return;  
    }
    buf[len]=0;
    Json::Reader reader;
    Json::Value msg;
    if(!reader.parse(buf,msg)){
    	perror("Error: invalid mesage!\n");
    	return;
    }
    switch(msg["type"].asInt()){
    	case 0:   // login
    	{
    		Json::Value info;
    		info["type"]=0;
    		int res=util->checkPassword(msg["name"].asString(), msg["password"].asString());
    		switch(res){
    			case 0:
    				info["body"]=0;       // OK
    				client_room_map[fd]=-1;
    				util->addOnlineUser(msg["name"].asString(), fd);
    				break;
    			case 1:
    				info["body"]=1;       // user does not exist
    				break;
    			case 2:
    				info["body"]=2;       // password does not match
    				break;
    		}	
    		string info_str = info.toStyledString();
    		write(fd, info_str.c_str(), info_str.size());
    		break;
    	}
    	case 1:  // jion room
    	{	 
    		int room_id=msg["body"].asInt();
    		for(map<int, int>::iterator it=client_room_map.begin();
    			                   it!=client_room_map.end();it++) {
    			if(it->first!=fd){
    				if(write(it->first,buf,len) < len)
    					perror("Something is wrong when write\n");
    			}
    		}
    		roomList[room_id]->addClient(fd);     // add to room
    		client_room_map[fd]=room_id;
    		break;
    	}
    	case 2:   // exit room
    	{
    		int room_id=client_room_map[fd];
    		roomList[room_id]->deleteClient(fd);   // delete from room
    		client_room_map[fd]=-1;
    		for(map<int, int>::iterator it=client_room_map.begin();
    			                   it!=client_room_map.end();it++) {
    			if(it->first!=fd){
    				if(write(it->first,buf,len) < len)
    					perror("Something is wrong when write\n");
    			}
    		}
    		break;
    	}
    	case 3:  // send message
    	{
    		int room_id=client_room_map[fd];
    		for(set<int>::iterator it=roomList[room_id]->begin();
    			                   it!=roomList[room_id]->end();it++) {
    			if(*it!=fd){
    				if(write(*it,buf,len) < len)
    					perror("Something is wrong when write\n");
    			}
    		}
    		break;
    	}  
    	case 4:  // register
    	{
    		int res = util->addUser(msg["name"].asString(), msg["password"].asString());
    		Json::Value info;
    		info["type"]=4;
    		info["body"]=res;
    		string info_str = info.toStyledString();
    		write(fd, info_str.c_str(), info_str.size());
    		break;
    	}
    	case 5:  // logout
    	{
    		util->deleteOnlineUser(fd);
    		break;
    	}
    }
}

void on_accept(int fd, short ev, void *arg)
{
	int client_fd;
	struct sockaddr_in client_addr;
	socklen_t client_len = sizeof(client_addr);
	client_fd = accept(fd, (struct sockaddr *)&client_addr, &client_len);
	if (client_fd < 0)
	{
		perror("accept failed");
		return;
	}
	printf("Accepted connection from %s   clien_id: %d\n", inet_ntoa(client_addr.sin_addr), client_fd);
	
	/* Set the client socket to non-blocking mode. */
	setnonblock(client_fd); //evutil_make_socket_nonblocking(client_fd);

	// 连接注册为新事件 (EV_PERSIST为事件触发后不默认删除)  
    struct event *pEvRead = event_new(evbase,client_fd,EV_READ|EV_PERSIST,onRead, pEvRead);   
    event_add(pEvRead, NULL);  

	// sent roomInfo to client
	Json::Value roomInfo;
	for(int i=0;i<roomNumber;i++)
	{
		roomInfo[i]=roomList[i]->getSize();
	}
	string msg = roomInfo.toStyledString();
	write(client_fd, msg.c_str(), msg.size());
}

int main(void)
{
	// Initialize chatting room info.
	for(int i=0;i<roomNumber;i++)
		roomList.push_back(new Room());

    util = Utils::getInstance();

	int listen_fd;
	struct sockaddr_in listen_addr;
	struct event ev_accept;
	int reuseaddr_on;

	/* Initialize libevent. */
	evbase = event_base_new();

	/* Create our listening socket. */
	listen_fd = socket(AF_INET, SOCK_STREAM, 0);
	if (listen_fd < 0)
	{
		perror("listen failed");
		return -1;
	}
	memset(&listen_addr, 0, sizeof(listen_addr));
	listen_addr.sin_family = AF_INET;
	listen_addr.sin_addr.s_addr = INADDR_ANY;
	listen_addr.sin_port = htons(SERVER_PORT);

	reuseaddr_on = 1;
	setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &reuseaddr_on, sizeof(reuseaddr_on));

	if (bind(listen_fd, (struct sockaddr *)&listen_addr, sizeof(listen_addr)) < 0)
	{
		perror("bind failed");
		return -1;
	}
	if (listen(listen_fd, 10) < 0)
	{
		perror("listen failed");
		return -1;
	}

	/* Set the socket to non-blocking, this is essential in event based programming with libevent. */
	setnonblock(listen_fd); //evutil_make_socket_nonblocking(listen_fd);

	/* We now have a listening socket, we create a read event to be notified when a client connects. */
	event_assign(&ev_accept, evbase, listen_fd, EV_READ | EV_PERSIST, on_accept, NULL);
	event_add(&ev_accept, NULL);

	/* Start the event loop. */
	printf("Server is running...\n");
	event_base_dispatch(evbase);
	return 0;
}
