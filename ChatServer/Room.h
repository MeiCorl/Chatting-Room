#include <set>
using namespace std;

class Room{
private:
    set<int> clients;                //  存放当前房间客户端链接
public:
    int getSize();
    set<int>::iterator begin();
    set<int>::iterator end();
    void addClient(int client_fd);
    void deleteClient(int client_fd);
};