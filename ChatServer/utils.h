#include <unordered_map>
#include <string>
using namespace std;

class Utils
{
private:
	const string user_info_path = "./user_info/user";
	static Utils* instance;
    unordered_map<string,string> passwd;    //  user_name --> password
    unordered_map<string, int>  user2fd;    //  user  --> client_fd
    unordered_map<int, string>  fd2user;    //  client_fd  --> user
    Utils();
public:
	static Utils* getInstance();
	int checkPassword(string user, string password);
	void addOnlineUser(string user, int fd);
	void deleteOnlineUser(int fd);
	int addUser(string user, string password);
	~Utils();
};