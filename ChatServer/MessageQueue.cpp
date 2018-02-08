#include "MessageQueue.h"

MessageQueue::MessageQueue(){}

MessageQueue::~MessageQueue(){}

void MessageQueue::push(Json::Value& val)
{
	this->mq.push(val);
}

Json::Value MessageQueue::pop()
{
	Json::Value val=this->mq.front();
	this->mq.pop();
	return val;
}

bool MessageQueue::isEmpty()
{
	return this->mq.empty();
}

int MessageQueue::size()
{
	return this->mq.size();
}

Json::Value& MessageQueue::front(){
	return this->mq.front();
}