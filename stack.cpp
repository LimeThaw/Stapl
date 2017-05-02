#ifndef STACK_CPP_INCLUDED
#define STACK_CPP_INCLUDED

#include<vector>

template<typename T>
class stack {
	public:
		stack() {}

		~stack() {}

		void push(const T &next) {
			if(data.size() >= 2048) {
				printf("Error: Stack grew too large!\n");
				exit(-1);
			}
			data.push_back(next);
		}

		T pop() {
			if(length() > 0) {
				T tmp = data.back();
				data.pop_back();
				return tmp;
			} else {
				return 0;
			}
		}

		T peek() {
			return data.back();
		}

		unsigned int length() {
			return data.size();
		}

		typename std::vector<T>::iterator begin() {
			return data.begin();
		}

		typename std::vector<T>::iterator end() {
			return data.end();
		}

	private:
		std::vector<T> data;
};

#endif