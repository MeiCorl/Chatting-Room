#include "Room.h"
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
#include <unordered_map>
        
const int SERVER_PORT = 1234;
const int roomNumber = 6;
vector<Room*> roomList;
map<int, int> client_room_map;    //   key: client_fd,   value: room_id
event_base *evbase; 

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
	char buf[1024];
	int len=read(fd,buf,1024);
	if (len <= 0) {  
        cout << "client closed" << endl;  
        // 连接结束(=0)或连接错误(<0)，将事件删除并释放内存空间
        client_room_map.erase(fd);
        close(fd);  
    //  struct event *pEvRead = (struct event*)arg; 
    //  event_del(pEvRead);  
    //  delete pEvRead;  
    //  event_free((struct event*)arg);
        return;  
    }
    buf[len]=0;
    cout << buf <<endl;
    Json::Reader reader;
    Json::Value msg;
    if(!reader.parse(buf,msg)){
    	perror("Error: invalid mesage!\n");
    	return;
    }
 // Json::Value info;
    switch(msg["type"].asInt()){
    	case 1:  
    	{	
    		cout<<"type 1"<<endl;  
    		int room_id=msg["body"].asInt();
    //		info["type"]=1;
    //		info["name"]="";
    //		info["body"]=room_id;
    //		string info_str = info.toStyledString();
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
    	case 2:   
    	{
    		cout<<"type 2"<<endl;
    		int room_id=client_room_map[fd];
    		roomList[room_id]->deleteClient(fd);   // delete from room
    		client_room_map[fd]=-1;
    	//	info["type"]=2;
    	//	info["name"]="";
    	//	info["body"]=room_id;
    	//	string info_str = info.toStyledString();
    		for(map<int, int>::iterator it=client_room_map.begin();
    			                   it!=client_room_map.end();it++) {
    			if(it->first!=fd){
    				if(write(it->first,buf,len) < len)
    					perror("Something is wrong when write\n");
    			}
    		}
    		break;
    	}
    	case 3:
    	{
    		cout<<"type 3"<<endl;
    		int room_id=client_room_map[fd];
    	//	info["type"]=3;
    	//	info["name"]=msg["name"].asString();
    	//	info["body"]=msg["body"].asString();
    	//	string info_str = info.toStyledString();
    		for(set<int>::iterator it=roomList[room_id]->begin();
    			                   it!=roomList[room_id]->end();it++) {
    			if(*it!=fd){
    				if(write(*it,buf,len) < len)
    					perror("Something is wrong when write\n");
    			}
    		}
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
	client_room_map[client_fd]=-1;
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