#include <queue>
#include <json/json.h>
using namespace std;

class MessageQueue
{
private:
	queue<Json::Value> mq;
public:
	MessageQueue();
	~MessageQueue();
	void push(Json::Value& val);
	Json::Value pop();
	bool isEmpty();
	int size();
	Json::Value& front();
};